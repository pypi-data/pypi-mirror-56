import numpy as np


class Estimator:

    def __init__(self):
        pass

    def forward(self, input):
        pass

    def loss_output(self, output, y):
        return np.sum(-np.log(output[y == 1])) / y.shape[0]

    def loss(self, input, y):
        output = self.forward(input)
        return self.loss_output(output, y)

    def backward(self, input, y):
        pass

    def evaluate(self, input, y):
        output = self.forward(input)
        predict_label_y = np.argmax(output, axis=-1)
        predict_y = np.eye(output.shape[1])[predict_label_y]

        loss = self.loss_output(output, y)
        label_y = np.argmax(y, axis=-1)
        accuracy = np.mean(predict_label_y == label_y)
        return predict_y, predict_label_y, loss, accuracy

    def predict(self, input):
        output = self.forward(input)
        predict_label_y = np.argmax(output, axis=-1)
        predict_y = np.eye(output.shape[0])[predict_label_y]

        return predict_y, predict_label_y


class CrossEntropy(Estimator):
    """
    if input is very small, -y/(input*y.shape[0]) maybe makes the result unstable. 
    because of it, we create softmax cross entropy estimator.
    """

    def __init__(self):
        Estimator.__init__(self)

    def forward(self, input):
        return input

    def backward(self, input, y):
        return -y/(input*y.shape[0])


class SoftmaxCrossEntropy(Estimator):
    """
    create softmax cross entropy estimator in order to make the numbers stable.
    """

    def __init__(self):
        Estimator.__init__(self)
        self._output = None

    def forward(self, input):
        e = np.exp(input - np.max(input, axis=-1, keepdims=True))
        s = np.sum(e, axis=-1, keepdims=True)
        self._output = e / s
        return self._output

    def backward(self, input, y):
        if self._output is None: self.forward(input)
        return (self._output - y)/y.shape[0]

