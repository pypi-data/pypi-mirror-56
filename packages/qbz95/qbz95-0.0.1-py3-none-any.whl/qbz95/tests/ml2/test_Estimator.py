import unittest
from qbz95.ml2.estimator import *
from qbz95.ml2.utils import *
import numpy as np


# logger.setLevel(level=logging.DEBUG)


class TestLayer(unittest.TestCase):
    def test_CrossEntropy(self):

        # Test the gradients w.r.t. params
        def compute_out_given(input, y):
            l = CrossEntropy()
            return l.loss(input, y)

        def compute_grad(input, y):
            l = CrossEntropy()
            grad = l.backward(input, y)
            return grad

        m, n = 10,6
        # when input is very small, it will make the -y/(input*y.shape[0]) unstable.
        # therefore, we add a number 0.001 and set decimal 3 instead of 6
        input = np.abs(np.random.randn(m, n))+0.001
        y = np.eye(n)[np.random.randint(n, size=m)]

        numeric_grad = eval_numerical_gradient(lambda input: compute_out_given(input, y), input)
        grad = compute_grad(input, y)

        print("numeric_grad[0,:]=", numeric_grad[:, :])
        print("grad[0,:]=", grad[:, :])

        np.testing.assert_array_almost_equal(numeric_grad, grad, decimal=3,
                                             err_msg="input gradient does not match numeric input gradient")

    def test_SoftmaxCrossEntropy(self):

        # Test the gradients w.r.t. params
        def compute_out_given(input, y):
            l = SoftmaxCrossEntropy()
            return l.loss(input, y)

        def compute_grad(input, y):
            l = SoftmaxCrossEntropy()
            grad = l.backward(input, y)
            return grad

        m, n = 10,6
        # now the grad is very stable.
        input = np.abs(np.random.randn(m, n))
        y = np.eye(n)[np.random.randint(n, size=m)]

        numeric_grad = eval_numerical_gradient(lambda input: compute_out_given(input, y), input)
        grad = compute_grad(input, y)

        print("numeric_grad[0,:]=", numeric_grad[:, :])
        print("grad[0,:]=", grad[:, :])

        np.testing.assert_array_almost_equal(numeric_grad, grad, decimal=6,
                                             err_msg="input gradient does not match numeric input gradient")