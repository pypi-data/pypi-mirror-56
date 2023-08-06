import numpy as np


class Initializer:
    def init(self, input_units, output_units):
        return np.random.randn(input_units, output_units)


class ScaleInitializer(Initializer):
    def __init__(self, scale=0.01):
        self.scale = scale

    def init(self, input_units, output_units):
        return np.random.randn(input_units, output_units) * self.scale


class XavierInitializer(Initializer):
    def init(self, input_units, output_units):
        return np.random.randn(input_units, output_units) / np.sqrt(input_units)


class HeInitializer(Initializer):
    def init(self, input_units, output_units):
        return np.random.randn(input_units, output_units) / np.sqrt(input_units / 2)


class GBInitializer(Initializer):
    """Glorot & Bengio"""
    def init(self, input_units, output_units):
        return np.random.randn(input_units, output_units) / np.sqrt((input_units + output_units) / 2)