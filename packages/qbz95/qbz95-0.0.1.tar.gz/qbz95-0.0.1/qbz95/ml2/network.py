import numpy as np
import time
from qbz95.ml2.estimator import *
from qbz95.ml2.layer import *
from qbz95.ml2.utils import *


class Network(object):

    def __init__(self, layers, estimator=SoftmaxCrossEntropy()):
        self.layers = layers
        self.estimator = estimator

    def forward(self, X, train_flag=True):
        """
        Compute activations of all network layers by applying them sequentially.
        Return a list of activations for each layer.
        Make sure last activation corresponds to network logits.
        """
        activations = []
        input = X

        for layer in self.layers:
            input = layer.forward(input, train_flag)
            activations.append(input)

        assert len(activations) == len(self.layers)
        output = self.estimator.forward(input)

        return activations, output

    def evaluate(self, X, y):
        _, output = self.forward(X, train_flag=False)
        predict_y, predict_label_y, loss, accuracy = self.estimator.evaluate(output, y)
        return predict_y, predict_label_y, loss, accuracy

    def predict(self, X):
        _, output = self.forward(X, train_flag=False)
        predict_y, predict_label_y = self.estimator.predict(output)
        return predict_y, predict_label_y

    def _train(self, X, Y):
        """
        Train your network on a given batch of X and y.
        You first need to run forward to get all layer activations.
        Then you can run layer.backward going from last to first layer.

        After you called backward for all layers, all Dense layers have already made one gradient step.
        """
        # very ingenious

        layer_activations, _ = self.forward(X)
        layer_inputs = [X] + layer_activations  
        layer_output = layer_activations[-1]

        loss_grad = self.estimator.backward(layer_output, Y)

        for i in reversed(range(len(self.layers))):
            loss_grad = self.layers[i].backward(layer_inputs[i], loss_grad)

    def train(self, X_train, Y_train, X_val=None, Y_val=None, epochs=10, batch_size=0, log_per_epoch=1):
        logs = {'train loss':[], 'train accuracy':[], 'val loss':[], 'val accuracy':[], 'over-fitting':[]}
        for epoch in range(epochs):
            start_time = time.time()
            for X_batch,Y_batch in iterate_minibatches(X_train, Y_train, batch_size=batch_size,shuffle=True):
                self._train(X_batch, Y_batch)

            _, _, train_loss, train_accuracy = self.evaluate(X_train, Y_train)
            _, _, val_loss, val_accuracy = self.evaluate(X_val, Y_val)

            log = "epoch: {} | {:.2f} seconds | " + \
                  "train loss: {:.4f} | train accuracy: {:.4f} | " + \
                  "val loss: {:.4f} | val accuracy: {:.4f} | " + \
                  "over-fitting: {:.4f}"

            print(log.format(epoch, time.time() - start_time, train_loss, train_accuracy,
                             val_loss, val_accuracy, train_accuracy - val_accuracy))

            if epoch % log_per_epoch == 0:
                logs['train loss'].append(train_loss)
                logs['train accuracy'].append(train_accuracy)
                logs['val loss'].append(val_loss)
                logs['val accuracy'].append(val_accuracy)
                logs['over-fitting'].append(train_accuracy - val_accuracy)

        return logs
