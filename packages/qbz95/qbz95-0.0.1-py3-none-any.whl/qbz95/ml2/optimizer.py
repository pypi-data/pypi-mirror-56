import numpy as np


class GradientOptimizer(object):
    def __init__(self, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.dW = None
        self.db = None

    def delta(self, grad_weights, grad_biases):
        self.grad_weights = grad_weights
        self.grad_biases = grad_biases
        return self.learning_rate * self.grad_weights, self.learning_rate * self.grad_biases


class MomentumOptimizer(GradientOptimizer):
    def __init__(self, learning_rate=0.1, beta=0.9):
        GradientOptimizer.__init__(self, learning_rate)
        assert (beta < 1)
        self.beta = beta

        self.initialized = False

        self.vW = None
        self.vb = None

    def delta(self, grad_weights, grad_biases):
        self.grad_weights = grad_weights
        self.grad_biases = grad_biases

        if not self.initialized:
            self.vW = np.zeros(grad_weights.shape)
            self.vb = np.zeros(grad_biases.shape)
            self.initialized = True

        self.vW = (self.beta * self.vW + (1 - self.beta) * self.grad_weights)
        self.vb = (self.beta * self.vb + (1 - self.beta) * self.grad_biases)
        return self.learning_rate * self.vW, self.learning_rate * self.vb


class RmspropOptimizer(object):
    def __init__(self, learning_rate=0.01, beta=0.9, epsilon=1e-8):
        GradientOptimizer.__init__(self, learning_rate)
        assert (beta < 1)
        self.beta = beta
        self.epsilon = epsilon

        self.initialized = False

        self.sW = None
        self.sb = None

    def delta(self, grad_weights, grad_biases):
        self.grad_weights = grad_weights
        self.grad_biases = grad_biases

        if not self.initialized:
            self.sW = np.zeros(grad_weights.shape)
            self.sb = np.zeros(grad_biases.shape)
            self.initialized = True

        self.sW = self.beta * self.sW + (1 - self.beta) * np.power(self.grad_weights, 2)
        self.sb = self.beta * self.sb + (1 - self.beta) * np.power(self.grad_biases, 2)

        deltaW = self.learning_rate * self.grad_weights / (np.sqrt(self.sW) + self.epsilon)
        deltaB = self.learning_rate * self.grad_biases / (np.sqrt(self.sb) + self.epsilon)
        return deltaW, deltaB


class AdamOptimizer(object):
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        GradientOptimizer.__init__(self, learning_rate)
        assert (beta1 < 1)
        assert (beta2 < 1)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon

        self.t = 0
        self.initialized = False

        self.vW = None
        self.sW = None
        self.vb = None
        self.sb = None

        self.vW_corrected = None
        self.sW_corrected = None
        self.vb_corrected = None
        self.sb_corrected = None

    def delta(self, grad_weights, grad_biases):
        self.grad_weights = grad_weights
        self.grad_biases = grad_biases

        if not self.initialized:
            self.vW = np.zeros(grad_weights.shape)
            self.sW = np.zeros(grad_weights.shape)
            self.vb = np.zeros(grad_biases.shape)
            self.sb = np.zeros(grad_biases.shape)
            self.initialized = True

        self.t = self.t + 1

        self.vW = self.beta1 * self.vW + (1 - self.beta1) * self.grad_weights
        self.sW = self.beta2 * self.sW + (1 - self.beta2) * np.power(self.grad_weights, 2)
        self.vb = self.beta1 * self.vb + (1 - self.beta1) * self.grad_biases
        self.sb = self.beta2 * self.sb + (1 - self.beta2) * np.power(self.grad_biases, 2)

        self.vW_corrected = self.vW / (1 - self.beta1 ** self.t)
        self.sW_corrected = self.sW / (1 - self.beta2 ** self.t)
        self.vb_corrected = self.vb / (1 - self.beta1 ** self.t)
        self.sb_corrected = self.sb / (1 - self.beta2 ** self.t)

        deltaW = self.learning_rate * self.vW_corrected / (np.sqrt(self.sW_corrected) + self.epsilon)
        deltaB = self.learning_rate * self.vb_corrected / (np.sqrt(self.sb_corrected) + self.epsilon)

        return deltaW, deltaB
