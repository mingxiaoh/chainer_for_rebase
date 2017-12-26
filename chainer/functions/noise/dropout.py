import numpy

import chainer
from chainer import configuration
from chainer import cuda
from chainer import function_node
from chainer import ia
from chainer.utils import argument
from chainer.utils import type_check


class Dropout(function_node.FunctionNode):

    """Dropout regularization."""

    def __init__(self, dropout_ratio):
        if not 0.0 <= dropout_ratio < 1.0:
            raise ValueError('dropout_ratio must be in the range [0, 1)')
        self.dropout_ratio = dropout_ratio

    def check_type_forward(self, in_types):
        type_check.expect(in_types.size() == 1)
        type_check.expect(in_types[0].dtype.kind == 'f')

    def forward_ia(self, inputs):
        x, = ia.to_mdarray((inputs[0],))
        mask, y = ia.dropout.Forward(x, self.dropout_ratio)
        self.mask = mask
        return y,

    def forward(self, x):
        # TODO: cosim
        if ia.all_ready(x, (2, 4)):
            return self.forward_ia(x)

        if hasattr(self, 'mask'):
            y = x[0] * self.mask
        else:
            scale = x[0].dtype.type(1. / (1 - self.dropout_ratio))
            xp = cuda.get_array_module(*x)
            if xp == numpy:
                flag = xp.random.rand(*x[0].shape) >= self.dropout_ratio
                self.mask = scale * flag
                y = x[0] * self.mask
            else:
                rand = xp.random.rand(*x[0].shape, dtype=numpy.float32)
                self.mask, y = cuda.elementwise(
                    'T x, R r, T scale, T ratio', 'T mask, T y',
                    '''
                    mask = (r >= ratio) * scale;
                    y = x * mask;
                    ''',
                    'dropout_fwd',
                )(x[0], rand, scale, self.dropout_ratio)
        return y,

    def backward(self, x, gy):
        return DropoutGrad(self.mask).apply(gy)


class DropoutGrad(function_node.FunctionNode):
    """Computes the gradient of the Dropout function."""

    def __init__(self, mask):
        self.mask = mask

    def forward_ia(self, inputs):
        gy, mask = ia.to_mdarray((inputs[0], self.mask))
        return ia.dropout.Backward(mask, gy),

    def forward(self, inputs):
        # TODO: cosim
        if ia.all_ready(inputs, (2, 4)):
            return self.forward_ia(inputs)
        y = inputs[0] * self.mask
        return y,

    def backward(self, indexes, gy):
        return DropoutGrad(self.mask).apply(gy)


def dropout(x, ratio=.5, **kwargs):
    """dropout(x, ratio=.5)

    Drops elements of input variable randomly.

    This function drops input elements randomly with probability ``ratio`` and
    scales the remaining elements by factor ``1 / (1 - ratio)``. In testing
    mode, it does nothing and just returns ``x``.

    .. warning::

       ``train`` argument is not supported anymore since v2.
       Instead, use ``chainer.using_config('train', boolean)``.
       See :func:`chainer.using_config`.

    Args:
        x (:class:`~chainer.Variable` or :class:`numpy.ndarray` or \
        :class:`cupy.ndarray`):
            Input variable. A :math:`(s_1, s_2, ..., s_N)` -shaped float array.
        ratio (float):
            Dropout ratio. The ``ratio`` must be ``0.0 <= ratio < 1.0``.

    Returns:
        ~chainer.Variable: Output variable.

    See the paper by G. Hinton: `Improving neural networks by preventing \
    co-adaptation of feature detectors <https://arxiv.org/abs/1207.0580>`_.

    .. admonition:: Example

        >>> x = np.array([[-1, 0], [2, -3], [-2, 1]], 'f')
        >>> with chainer.using_config('train', True):
        ...     y = F.dropout(x)
        >>> y.data
        array([[-2.,  0.],
               [ 4., -6.],
               [-0.,  2.]], dtype=float32)
        >>> with chainer.using_config('train', True):
        ...     y = F.dropout(x, ratio=0.0) \
# dropout returns original input if ratio=0.0
        >>> (x == y.data).all()
        True
        >>> with chainer.using_config('train', False):
        ...     y = F.dropout(x) \
# dropout in test mode returns original input
        >>> (x == y.data).all()
        True

    """
    argument.check_unexpected_kwargs(
        kwargs, train='train argument is not supported anymore. '
        'Use chainer.using_config')
    argument.assert_kwargs_empty(kwargs)

    if configuration.config.train:
        return Dropout(ratio).apply((x,))[0]
    return chainer.as_variable(x)
