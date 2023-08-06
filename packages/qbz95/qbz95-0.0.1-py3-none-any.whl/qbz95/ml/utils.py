import numpy as np
import logging
import pandas as pd
import matplotlib.pyplot as plt
from qbz95.ml.planar_utils import plot_decision_boundary

#
# function out = mapFeature(X1, X2)
# % MAPFEATURE Feature mapping function to polynomial features
# %
# %   MAPFEATURE(X1, X2) maps the two input features
# %   to quadratic features used in the regularization exercise.
# %
# %   Returns a new feature array with more features, comprising of
# %   X1, X2, X1.^2, X2.^2, X1*X2, X1*X2.^2, etc..
# %
# %   Inputs X1, X2 must be the same size
# %
# degree = 6;
# out = ones(size(X1(:,1)));
# for i = 1:degree
#     for j = 0:i
#         out(:, end+1) = (X1.^(i-j)).*(X2.^j);
#     end
# end
#
# end

def add_intercept(X):
    m = X.shape[1]
    X = np.row_stack((np.ones((1, m)), X))
    return X


def feature_normalize(X):
    mu = np.mean(X, axis=1, keepdims=True)
    sigma = np.std(X, axis=1, keepdims=True, ddof=1)  # Means Delta Degrees of Freedom, need to define a freedom
    X = (X - mu)/sigma
    return X, mu, sigma


def get_logger():
    logger1 = logging.getLogger("ml")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger1.addHandler(handler)
    logger1.setLevel(logging.INFO)
    return logger1


logger = get_logger()


def check_debug_mode(level, epoch_times, print_num_epoch, keep_cost_num_epoch):
    logger.setLevel(level=level)
    if level == logging.DEBUG:
        epoch_times = 1
        print_num_epoch = 1
        keep_cost_num_epoch = 1
    return epoch_times, print_num_epoch, keep_cost_num_epoch


class NumberIterator(object):
    def __init__(self, num_epochs=100):
        assert(num_epochs > 0)
        self.start_flag = False
        self.epoch_times = 0
        self.num_epochs = num_epochs

    def iterate(self):
        if self.start_flag :
            self.epoch_times = self.epoch_times + 1
        else:
            self.start_flag = True
        if self.epoch_times >= self.num_epochs:
            return False
        else:
            return True


class MeanSquaredError(object):

    @classmethod
    def cost(cls, A, Y):
        m = Y.shape[1]
        return np.sum(np.power(A-Y, 2))/2/m

    @classmethod
    def gradient_cost(cls, A, Y):
        m = Y.shape[1]
        return (A-Y)/m


class SigmoidCrossEntropy(object):
    @classmethod
    def cost(cls, A, Y):
        m = Y.shape[1]
        return -np.nansum(np.multiply(Y, np.log(A)) + np.multiply(1-Y, np.log(1-A)))/m

    @classmethod
    def gradient_cost(cls, A, Y):
        m = Y.shape[1]
        return (A-Y)/m


class SoftmaxCrossEntropy(object):
    @classmethod
    def cost(cls, A, Y):
        m = Y.shape[1]
        return -np.sum(np.multiply(Y, np.log(A)))/m

    @classmethod
    def gradient_cost(cls, A, Y):
        m = Y.shape[1]
        return (A-Y)/m


class Linear(object):

    @classmethod
    def activate(cls, Z):
        return Z

    @classmethod
    def gradient(cls, Z):
        A = cls.activate(Z)
        return np.ones(A.shape)


class Relu(object):

    @classmethod
    def activate(cls, Z):
        return np.maximum(0, Z)

    @classmethod
    def gradient(cls, Z):
        A = cls.activate(Z)
        return np.int64(A > 0)


def sigmoid(x, w=None):
    if w is None:
        z = x
    else:
        z = np.dot(x, w)
    return 1.0 / (1.0 + np.exp(-z))


class Sigmoid(object):

    @classmethod
    def activate(cls, Z):
        return sigmoid(Z)

    @classmethod
    def gradient(cls, Z):
        A = cls.activate(Z)
        return np.multiply(A, 1-A)


class Tanh(object):

    @classmethod
    def activate(cls, Z):
        return np.tanh(Z)

    @classmethod
    def gradient(cls, Z):
        A = cls.activate(Z)
        return 1 - np.power(A, 2)

    # @classmethod
    # def gradient_cost(cls, A, Y):
    #     pass


class Softmax(object):
    @classmethod
    def activate(cls, Z):
        E = np.exp(Z)
        return E/np.sum(E, axis = 0, keepdims = True)

    @classmethod
    def gradient(cls, Z):
        A = cls.activate(Z)
        return np.multiply(A, (1-A))

    # @classmethod
    # def compute_cost(cls, A, Y):
    #     m = Y.shape[1]
    #     return -np.sum(np.multiply(Y, np.log(A)))/m

    # @classmethod
    # def gradient_cost(cls, A, Y):
    #     m = Y.shape[1]
    #     return (A-Y)/m


class WeightInitializer(object):

    def get_scale(self, num_neuron, num_weights):
        return 0

    def initial_weights(self, num_neuron, num_weights):
        scale = self.get_scale(num_neuron, num_weights)
        if scale==0:
            return np.zeros((num_neuron, num_weights)), np.zeros((num_neuron, 1))
        else:
            return np.random.randn(num_neuron, num_weights) * scale, np.zeros((num_neuron, 1))


class StaticWeightInitializer(WeightInitializer):

    def __init__(self, scale=0.01):
        self.scale = scale

    def get_scale(self, num_neuron, num_weights):
        return self.scale


class HeWeightInitializer(WeightInitializer):
    def get_scale(self, num_neuron, num_weights):
        return np.sqrt(2.0/num_weights)


class XavierWeightInitializer(WeightInitializer):
    def get_scale(self, num_neuron, num_weights):
        return np.sqrt(1.0/num_weights)


class GbWeightInitializer(WeightInitializer):
    def get_scale(self, num_neuron, num_weights):
        return np.sqrt(2.0/(num_neuron+num_weights))


class Regularizer(object):

    def __init__(self, alpha=0):
        self.alpha = alpha

    def regularize(self, m, W):
        return 0

    def gradient(self, m, W):
        return 0


class L2Regularizer(Regularizer):

    def __init__(self, alpha=0.001):
        Regularizer.__init__(self, alpha)

    def regularize(self, m, W):
        return self.alpha * np.sum(np.multiply(W, W)) / (2 * m)

    def gradient(self, m, W):
        return self.alpha * W / m


class L1Regularizer(Regularizer):

    def __init__(self, alpha=0.001):
        Regularizer.__init__(self, alpha)

    def regularize(self, m, W):
        return self.alpha * np.sum(np.abs(W)) / m

    def gradient(self, m, W):
        return self.alpha * W / np.abs(W) / m


class GradientOptimizer(object):
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def initialize(self, layer):
        pass

    def update_parameters(self, layer):
        layer.t = layer.t + 1
        layer.W = layer.W - self.learning_rate * layer.dW
        layer.b = layer.b - self.learning_rate * layer.db


class MomentumOptimizer(GradientOptimizer):
    def __init__(self, learning_rate=0.01, beta=0):
        GradientOptimizer.__init__(self, learning_rate)
        assert (beta < 1)
        self.beta = beta

    def initialize(self, layer):
        layer.vW = np.zeros(layer.dW.shape)
        layer.vb = np.zeros(layer.db.shape)

    def update_parameters(self, layer):
        layer.t = layer.t + 1

        layer.vW = (self.beta * layer.vW + (1 - self.beta) * layer.dW)
        layer.vb = (self.beta * layer.vb + (1 - self.beta) * layer.db)
        layer.W = layer.W - self.learning_rate * layer.vW
        layer.b = layer.b - self.learning_rate * layer.vb


# Nesterov Accelerated Gradient
class NagOptimizer(GradientOptimizer):
    pass
    # def __init__(self, learning_rate=0.01, beta=0):
    #     GradientOptimizer.__init__(self, learning_rate)
    #     assert (beta < 1)
    #     self.beta = beta
    #
    # def initialize(self, layer):
    #     layer.vW = np.zeros(layer.dW.shape)
    #     layer.vb = np.zeros(layer.db.shape)
    #
    # def update_parameters(self, layer):
    #     layer.t = layer.t + 1
    #
    #     layer.vW = (self.beta * layer.vW + (1 - self.beta) * layer.dW)
    #     layer.vb = (self.beta * layer.vb + (1 - self.beta) * layer.db)
    #     layer.W = layer.W - self.learning_rate * layer.vW
    #     layer.b = layer.b - self.learning_rate * layer.vb


class AdamOptimizer(object):
    def __init__(self, learning_rate=0.01, beta1=0, beta2=0, epsilon=1e-8):
        GradientOptimizer.__init__(self, learning_rate)
        assert (beta1 < 1)
        assert (beta2 < 1)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon

    def initialize(self, layer):
        layer.vW = np.zeros(layer.dW.shape)
        layer.sW = np.zeros(layer.dW.shape)
        layer.vb = np.zeros(layer.db.shape)
        layer.sb = np.zeros(layer.db.shape)

    def update_parameters(self, layer):
        layer.t = layer.t + 1

        layer.vW = self.beta1 * layer.vW + (1-self.beta1) * layer.dW
        layer.sW = self.beta2 * layer.sW + (1 - self.beta2) * np.power(layer.dW, 2)
        layer.vb = self.beta1 * layer.vb + (1-self.beta1) * layer.db
        layer.sb = self.beta2 * layer.sb + (1 - self.beta2) * np.power(layer.db, 2)

        layer.vW_corrected = layer.vW/(1 - self.beta1 ** layer.t)
        layer.sW_corrected = layer.sW/(1 - self.beta2 ** layer.t)
        layer.vb_corrected = layer.vb/(1 - self.beta1 ** layer.t)
        layer.sb_corrected = layer.sb/(1 - self.beta2 ** layer.t)

        layer.W = layer.W - self.learning_rate*layer.vW_corrected/(np.sqrt(layer.sW_corrected) + self.epsilon)
        layer.b = layer.b - self.learning_rate*layer.vb_corrected/(np.sqrt(layer.sb_corrected) + self.epsilon)


