import numpy as np


class Regularizer(object):

    def __init__(self, alpha=0):
        self.alpha = alpha

    def regularize(self, weights):
        return 0

    def gradient(self, weights):
        return 0


class L2Regularizer(Regularizer):

    def __init__(self, alpha=0.001):
        Regularizer.__init__(self, alpha)

    def regularize(self, weights):
        return self.alpha * np.sum(np.multiply(weights, weights)) / 2

    def gradient(self, weights):
        return self.alpha * weights


class L1Regularizer(Regularizer):

    def __init__(self, alpha=0.001):
        Regularizer.__init__(self, alpha)

    def regularize(self, weights):
        return self.alpha * np.sum(np.abs(weights))

    def gradient(self, weights):
        return self.alpha * weights / np.abs(weights)
