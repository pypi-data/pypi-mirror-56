import numpy as np
from qbz95.ml2.optimizer import *
from qbz95.ml2.initializer import *
from qbz95.ml2.regularizer import *


class Layer:
    """
    A building block. Each layer is capable of performing two things:

    - Process input to get output:           output = layer.forward(input)

    - Propagate gradients through itself:    grad_input = layer.backward(input, grad_output)

    Some layers also have learnable parameters which they update during layer.backward.
    """

    def __init__(self):
        pass

    def forward(self, input, train_flag=True):
        return input

    def backward(self, input, grad_output):
        num_units = input.shape[1]
        d_layer_d_input = np.eye(num_units)
        return np.dot(grad_output, d_layer_d_input)  # chain rule


class ReLU(Layer):
    '''Rectified Linear Unit'''
    def __init__(self):
        """ReLU layer simply applies elementwise rectified linear unit to all inputs"""
        Layer.__init__(self)

    def forward(self, input, train_flag=True):
        """Apply elementwise ReLU to [batch, input_units] matrix"""
        return np.maximum(0, input)

    def backward(self, input, grad_output):
        """Compute gradient of loss w.r.t. ReLU input"""
        relu_grad = input > 0
        return grad_output * relu_grad


class Sigmoid(Layer):
    def __init__(self):
        Layer.__init__(self)
        self._output = None

    def forward(self, input, train_flag=True):
        self._output = 1.0 / (1.0 + np.exp(-input))
        return self._output

    def backward(self, input, grad_output):
        if self._output is None: self.forward(input)
        return self._output * (1 - self._output) * grad_output


class Tanh(Layer):
    def __init__(self):
        Layer.__init__(self)
        self._output = None

    def forward(self, input, train_flag=True):
        self._output = np.tanh(input)
        return self._output

    def backward(self, input, grad_output):
        if self._output is None: self.forward(input)
        return (1.0 - np.power(self._output, 2)) * grad_output


class BatchNormalization(Layer):
    def __init__(self, epsilon=1e-8):
        Layer.__init__(self)

        self.epsilon = epsilon
        self.gamma = None
        self.beta = None
        self.t = 0
        self.mu = None
        self.var = None
        self.k = 0
        self.batch_size = 0

        self.initialized = False

    def initial_params(self, var, mu):
        self.gamma = var
        self.beta = mu
        self.initialized = True

    def update_mu_var(self, mu, var, m):
        self.k = self.k + 1
        self.mu = ((self.k - 1)*self.mu + mu)/self.k if self.mu is not None else mu
        self.var = ((self.k - 1)*self.var + m*var/max(1, m-1))/self.k if self.var is not None else m*var/max(1, m-1)

    def compute(self, input):
        mu = np.mean(input, axis=0)
        var = np.mean(np.power(input - mu, 2), axis=0)
        x = (input - mu) / np.sqrt(var + self.epsilon)
        return mu, var, x

    def forward(self, input, train_flag=True):
        # if train_flag:
        if train_flag:
            mu, var, x = self.compute(input)
            self.update_mu_var(mu, var, input.shape[0])
            if not self.initialized:
                self.initial_params(var, mu)
                return input
            else:
               return self.gamma * x + self.beta
        else:
            assert(self.mu is not None and self.var is not None)

            x = (input - self.mu) / np.sqrt(self.var + self.epsilon)
            return self.gamma * x + self.beta

    def backward(self, input, grad_output):
        mu, var, x = self.compute(input)

        if not self.initialized:
            self.initial_params(var, mu)

        grad_gamma = np.sum(grad_output * x, axis=0)
        grad_beta = np.sum(grad_output, axis=0)

        grad_input = self.gamma / np.sqrt(var + self.epsilon) * (grad_output - np.mean(grad_output, axis=0)) - \
                     self.gamma / np.power(var + self.epsilon, 1.5) * (input - mu) * np.mean(grad_output * (input - mu),
                                                                                             axis=0)
        self.gamma = self.gamma - grad_gamma
        self.beta = self.beta - grad_beta

        return grad_input


class MomentumBatchNormalization(BatchNormalization):
    def __init__(self, epsilon=1e-8, decay = 0.99):
        BatchNormalization.__init__(self, epsilon)
        self.decay = decay

    def update_mu_var(self, mu, var, m):
        if self.mu is None: self.mu = np.zeros(mu.shape)
        if self.var is None: self.var = np.zeros(var.shape)
        self.mu = self.decay*self.mu + (1-self.decay)*mu
        self.var = self.decay*self.var + (1-self.decay)*var


class Dropout(Layer):
    def __init__(self, drop_probability=0.1):
        Layer.__init__(self)
        self.drop_probability = drop_probability
        self.keep_probability = 1 - drop_probability

        assert 0 <= self.keep_probability <= 1

        self.mask = None

    def forward(self, input, train_flag=True):
        if train_flag:
            if self.drop_probability == 0:
                return input
            elif self.drop_probability == 1:
                return input.zeros_like()
            else:
                self.mask = np.random.uniform(0, 1.0, input.shape) < self.keep_probability
                return self.mask * input / self.keep_probability
        else:
            return input

    def backward(self, input, grad_output):
        if self.drop_probability == 0:
            return grad_output
        elif self.drop_probability == 1:
            return grad_output.zeros_like()
        else:
            if self.mask is None:
                self.mask = np.random.uniform(0, 1.0, input.shape) < self.keep_probability
            return self.mask * grad_output / self.keep_probability


class Softmax(Layer):
    def __init__(self):
        """
        Softmax

        I think that softmax can be independent from cross entropy
        """
        Layer.__init__(self)
        self._output = None

    def forward(self, input, train_flag=True):
        # e = np.exp(input)
        # s = np.sum(input, axis=-1, keepdims=True)
        # more numerical stability method below
        e = np.exp(input - np.max(input, axis=-1, keepdims=True))
        s = np.sum(e, axis=-1, keepdims=True)
        self._output = e / s
        return self._output

    def backward(self, input, grad_output):
        if self._output is None: self.forward(input)
        x =  self._output * grad_output
        return x - self._output * np.sum(x, axis=-1, keepdims=True)


class Dense(Layer):
    def __init__(self, input_units, output_units, initializer=ScaleInitializer(0.01), regularizer=Regularizer(),
                 optimizer=GradientOptimizer(learning_rate=0.1)):
        """
        A dense layer is a layer which performs a learned affine transformation:
        f(x) = <W*x> + b
        """
        Layer.__init__(self)

        self.weights = initializer.init(input_units, output_units)
        self.biases = np.zeros(output_units)
        self.regularizer = regularizer
        self.optimizer = optimizer

    def forward(self, input, train_flag=True):
        """
        Perform an affine transformation:
        f(x) = <W*x> + b

        input shape: [batch, input_units]
        output shape: [batch, output units]
        """
        return input.dot(self.weights) + self.biases

    def backward(self, input, grad_output):
        # compute d f / d x = d f / d dense * d dense / d x
        # where d dense/ d x = weights transposed
        grad_input = grad_output.dot(self.weights.T)

        # compute gradient w.r.t. weights and biases
        grad_weights = input.T.dot(grad_output) + self.regularizer.gradient(self.weights)  #/ input.shape[0]
        grad_biases = np.sum(grad_output, axis=0) #/ input.shape[0]

        assert grad_weights.shape == self.weights.shape and grad_biases.shape == self.biases.shape
        # Here we perform a stochastic gradient descent step.
        # Later on, you can try replacing that with something better.
        delta_weights, delta_biases = self.optimizer.delta(grad_weights, grad_biases)
        self.weights = self.weights - delta_weights
        self.biases = self.biases - delta_biases

        return grad_input

