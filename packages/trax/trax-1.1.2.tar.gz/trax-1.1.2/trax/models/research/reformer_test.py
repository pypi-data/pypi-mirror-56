# coding=utf-8
# Copyright 2019 The Trax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for Transformer-Revnet models."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest
from absl.testing import parameterized
import jax
import numpy as onp

from trax import backend
from trax import layers as tl
from trax.backend import numpy as np
from trax.models.research import reformer
from trax.shapes import ShapeDtype


class PoisonOnRNGMismatchAttention(tl.BaseCausalAttention):
  """Fills gradients with NaNs if reverse rng does not match forward rng."""

  # pylint: disable=protected-access
  def forward_and_backward(self, inputs, ct, rng=None, **kwargs):
    assert backend.get_name() == 'jax', (
        'JAX backend is required to use forward_and_backward.')

    if ct is not None and tl.Layer._STASH_OUT is not None:
      recovered_rng = tl.Layer._STASH_OUT.pop(self)
      is_same = (rng[0] == recovered_rng[0]) & (rng[1] == recovered_rng[1])
      is_same = is_same.astype(np.float32)
      # Divides by zero if rngs are not the same, which results in NaNs.
      inputs = (inputs[0] / is_same, inputs[1] / is_same, inputs[2] / is_same)

    def _do_forward(x):  # pylint: disable=invalid-name
      res, _ = self.forward_with_state(x, rng=rng, **kwargs)
      return res
    output, vjpfun = jax.vjp(_do_forward, inputs)
    return output, vjpfun(ct)[0]

  def forward_with_state(self, inputs, weights=(), state=(),
                         rng=None, **kwargs):
    if tl.Layer._STASH_IN is not None:
      tl.Layer._STASH_IN[self] = rng
    return inputs[2], state
  # pylint: enable=protected-access


class ReformerTest(parameterized.TestCase):

  def test_reformer_lm_forward_shape(self):
    """Run the ReformerLM forward and check output shape."""
    vocab_size = 16
    input_sd = ShapeDtype((1, 8), np.int32)
    input_signature = (input_sd, input_sd)
    model = reformer.ReformerLM(
        vocab_size, d_model=32, d_ff=64,
        d_attention_key=16, d_attention_value=16, n_layers=1, n_heads=2,
        max_len=16, n_chunks=2, n_attention_chunks=1)
    final_shape = tl.check_shape_agreement(
        model, input_signature)
    self.assertEqual(((1, 8, 16), (1, 8, 16)), final_shape)

  def test_reformer_rng_consistency(self):
    with backend.use_backend('jax'):
      vocab_size = 16
      batch_size = 1
      input_sd = ShapeDtype((batch_size, 8), np.int32)
      input_signature = (input_sd, input_sd)
      model = reformer.ReformerLM(
          vocab_size, d_model=32, d_ff=64,
          d_attention_key=16, d_attention_value=16, n_layers=1, n_heads=2,
          max_len=16, n_chunks=2, n_attention_chunks=1, mode='train',
          attention_type=PoisonOnRNGMismatchAttention)

      rng = backend.random.get_prng(0)
      weights, state = model.init(input_signature)

      def dummy_loss_fn(weights):
        inputs = (np.zeros(input_sd.shape, dtype=np.int32),) * 2
        output = model(inputs, weights=weights, state=state, rng=rng)
        dummy_loss = backend.numpy.sum(output[0])
        return dummy_loss

      grad_fn = backend.grad(dummy_loss_fn)
      grads = grad_fn(weights)
      # PoisonOnRNGMismatchAttention uses NaNs to signal an rng mismatch.
      for grad in jax.tree_util.tree_leaves(grads):
        assert onp.all(onp.isfinite(grad))


if __name__ == '__main__':
  absltest.main()
