import unittest
from qbz95.ml2.layer import *
from qbz95.ml2.utils import *
import numpy as np


# logger.setLevel(level=logging.DEBUG)


class TestLayer(unittest.TestCase):
    def test_ReLU(self):
        np.random.seed(320)

        grad_output = np.random.randn(10, 32)
        x = np.random.randn(10, 32)
        l = ReLU()
        grads = l.backward(x, grad_output)
        numeric_grads = eval_numerical_gradient(lambda x: np.sum(l.forward(x) * grad_output), x=x)
        # print(grads[2,:])
        # print(numeric_grads[2,:])
        np.testing.assert_array_almost_equal(grads, numeric_grads, decimal=6, \
                                             err_msg = "gradient returned by your layer does not match the numerically computed gradient")

    def test_Sigmoid(self):
        np.random.seed(320)
        grad_output = np.random.randn(10, 32)
        x = np.linspace(-1, 1, 10 * 32).reshape([10, 32])
        l = Sigmoid()
        grads = l.backward(x, grad_output)
        numeric_grads = eval_numerical_gradient(lambda x: np.sum(l.forward(x) * grad_output), x=x)
        np.testing.assert_array_almost_equal(grads, numeric_grads, decimal=6, \
                                             err_msg="gradient returned by your layer does not match the numerically computed gradient")


    def test_Tanh(self):
        np.random.seed(320)
        grad_output = np.random.randn(10, 32)
        x = np.linspace(-1, 1, 10 * 32).reshape([10, 32])
        l = Tanh()
        grads = l.backward(x, grad_output)
        numeric_grads = eval_numerical_gradient(lambda x: np.sum(l.forward(x) * grad_output), x=x)
        np.testing.assert_array_almost_equal(grads, numeric_grads, decimal=6, \
                                             err_msg="gradient returned by your layer does not match the numerically computed gradient")

    def test_Dense(self):
        l = Dense(128, 150)

        assert -0.05 < l.weights.mean() < 0.05 and 1e-3 < l.weights.std() < 1e-1, \
            "The initial weights must have zero mean and small variance. " \
            "If you know what you're doing, remove this assertion."
        assert -0.05 < l.biases.mean() < 0.05, "Biases must be zero mean. Ignore if you have a reason to do otherwise."

        # To test the outputs, we explicitly set weights with fixed values. DO NOT DO THAT IN ACTUAL NETWORK!
        l = Dense(3, 4)

        x = np.linspace(-1, 1, 2 * 3).reshape([2, 3])
        l.weights = np.linspace(-1, 1, 3 * 4).reshape([3, 4])
        l.biases = np.linspace(-1, 1, 4)

        assert np.allclose(l.forward(x), np.array([[0.07272727, 0.41212121, 0.75151515, 1.09090909],
                                                   [-0.90909091, 0.08484848, 1.07878788, 2.07272727]]))
        print("Well done!")

        x = np.linspace(-1, 1, 10 * 32).reshape([10, 32])
        l = Dense(32, 64, optimizer=GradientOptimizer(learning_rate=0))

        numeric_grads = eval_numerical_gradient(lambda x: l.forward(x).sum(), x)
        grads = l.backward(x, np.ones([10, 64]))

        assert np.allclose(grads, numeric_grads, rtol=1e-3, atol=0), "input gradient does not match numeric grad"
        print("Well done!")

        # Test the gradients w.r.t. params
        def compute_out_given_wb(w, b):
            l = Dense(32, 64, optimizer=GradientOptimizer(learning_rate=1))
            l.weights = np.array(w)
            l.biases = np.array(b)
            x = np.linspace(-1, 1, 10 * 32).reshape([10, 32])
            return l.forward(x)

        def compute_grad_by_params(w, b):
            l = Dense(32, 64, optimizer=GradientOptimizer(learning_rate=1))
            l.weights = np.array(w)
            l.biases = np.array(b)
            x = np.linspace(-1, 1, 10 * 32).reshape([10, 32])
            l.backward(x, np.ones([10, 64]))
            return w - l.weights, b - l.biases

        w, b = np.random.randn(32, 64), np.linspace(-1, 1, 64)

        numeric_dw = eval_numerical_gradient(lambda w: compute_out_given_wb(w, b).sum(), w)
        numeric_db = eval_numerical_gradient(lambda b: compute_out_given_wb(w, b).sum(), b)
        grad_w, grad_b = compute_grad_by_params(w, b)

        np.testing.assert_array_almost_equal(numeric_dw, grad_w, decimal=6, err_msg="weight gradient does not match numeric weight gradient")
        np.testing.assert_array_almost_equal(numeric_db, grad_b, decimal=6, err_msg="weight gradient does not match numeric weight gradient")
        print("Well done!")

    def test_BatchNormalization(self):
        # Test the gradients w.r.t. params
        def compute_out_given(gamma, beta, x, grad_out):
            l = BatchNormalization()
            l.initial_params(gamma, beta)
            return np.sum(l.forward(x) * grad_out)

        def compute_grad(gamma, beta, x, grad_out):
            l = BatchNormalization()
            l.initial_params(gamma, beta)
            grad_x = l.backward(x, grad_out)
            return gamma - l.gamma, beta - l.beta, grad_x

        m, n = 16, 24
        gamma = np.random.randn(1, n)
        beta = np.random.randn(1, n)
        x = np.random.randn(m, n)
        grad_out = np.linspace(-1, 1, m * n).reshape(m, n)

        numeric_dgamma = eval_numerical_gradient(lambda gamma: compute_out_given(gamma, beta, x, grad_out), gamma)
        numeric_dbeta = eval_numerical_gradient(lambda beta: compute_out_given(gamma, beta, x, grad_out), beta)
        numeric_dx = eval_numerical_gradient(lambda x: compute_out_given(gamma, beta, x, grad_out), x)
        grad_gamma, grad_beta, grad_x = compute_grad(gamma, beta, x, grad_out)

        print("grad_x[0,:]=", grad_x[0, :])

        assert np.allclose(numeric_dgamma, grad_gamma, rtol=1e-3, \
                           atol=0), "gamma gradient does not match numeric gamma gradient"
        assert np.allclose(numeric_dbeta, grad_beta, rtol=1e-3, \
                           atol=0), "beta gradient does not match numeric beta gradient"
        assert np.allclose(numeric_dx, grad_x, rtol=1e-3, \
                           atol=0), "input gradient does not match numeric input gradient"

    def test_BatchNormalization1(self):
        """test mu and var of inference"""

        m, n, k = 16, 8, 10

        l = BatchNormalization()
        mu_array= np.zeros((k, n))
        var_array = np.zeros((k, n))
        mu_infer_array = np.zeros((k, n))
        var_infer_array = np.zeros((k, n))

        for i in range(k):
            input = np.random.permutation(m*n).reshape(m, n)

            mu, var, x = l.compute(input)
            l.forward(input)

            mu_array[i] = mu
            var_array[i] = var
            mu_infer_array[i] = l.mu
            var_infer_array[i] = l.var

        np.testing.assert_array_almost_equal(mu_infer_array, np.cumsum(mu_array, axis=0)/(np.arange(0, k)+1).reshape(k, 1), decimal=6,
                                             err_msg="mu_infer should be the mean of mu")
        np.testing.assert_array_almost_equal(var_infer_array, m/(m-1)*np.cumsum(var_array, axis=0)/(np.arange(0, k)+1).reshape(k, 1), decimal=6,
                                             err_msg="var_infer should be the mean of var")

    def test_Dropout(self):
        seed = 257
        # Test the gradients w.r.t. params
        def compute_out_given(x, grad_out):
            l = Dropout(drop_probability=0.5)
            np.random.seed(seed)
            return np.sum(l.forward(x) * grad_out)

        def compute_grad(x, grad_out):
            l = Dropout(drop_probability=0.5)
            np.random.seed(seed)
            grad_x = l.backward(x, grad_out)
            return grad_x

        m, n = 16, 24
        x = np.random.randn(m, n)
        grad_out = np.linspace(-1, 1, m * n).reshape(m, n)

        numeric_dx = eval_numerical_gradient(lambda x: compute_out_given(x, grad_out), x)
        grad_x = compute_grad(x, grad_out)

        print("grad_x[0,:]=", grad_x[0, :])

        np.testing.assert_array_almost_equal(numeric_dx, grad_x, decimal=6, err_msg="input gradient does not match numeric input gradient")


    def test_Softmax(self):
        seed = 257
        # Test the gradients w.r.t. params
        def compute_out_given(x, grad_out):
            l = Softmax()
            return np.sum(l.forward(x) * grad_out)

        def compute_grad(x, grad_out):
            l = Softmax()
            grad_x = l.backward(x, grad_out)
            return grad_x

        m, n = 16, 24
        x = np.random.randn(m, n)
        grad_out = np.linspace(-1, 1, m * n).reshape(m, n)

        numeric_dx = eval_numerical_gradient(lambda x: compute_out_given(x, grad_out), x)
        grad_x = compute_grad(x, grad_out)

        print("grad_x[0,:]=", grad_x[0, :])

        np.testing.assert_array_almost_equal(numeric_dx, grad_x, decimal=6, err_msg="input gradient does not match numeric input gradient")