import numpy as np
from qbz95.ml.utils import *
from qbz95.ml.model import Model


class LinearModel(Model):
    def __init__(self, num_features,
                 activator=Sigmoid, regularizer=Regularizer(), iterator=NumberIterator(100),
                 optimizer=GradientOptimizer(0.001), initializer=StaticWeightInitializer(0.01),
                 keep_cost_num_epoch=1000, cost_object=SigmoidCrossEntropy):
        """
            Args:
                num_features -- number of features
                activator -- activator
                regularizer -- regularizer
                iterator -- iterator
                optimizer -- optimizer
                initializer -- initializer
        """
        Model.__init__(self)
        self.num_features = num_features
        self.activator = activator
        self.regularizer = regularizer
        self.iterator = iterator
        self.optimizer = optimizer
        self.initializer = initializer
        self.mini_batch = 0
        self.keep_cost_num_epoch = keep_cost_num_epoch
        self.W, self.b = self.initializer.initial_weights(1, num_features)
        self.b = np.asscalar(self.b)
        self.cost = None
        self.dw = None
        self.db = None
        self.z = None
        self.a = None
        self.dz = None
        self.da = None
        self.has_run_fit = False
        self.t = 0
        self.cost_object = cost_object

    def compute_cost(self, X, y):
        m = X.shape[1]
        self.z = np.dot(self.W, X) + self.b
        self.a = self.activator.activate(self.z)
        self.cost = self.cost_object.cost(self.a, y) + self.regularizer.regularize(m, self.W)

    def activate(self, X):
        assert self.has_run_fit
        z = np.dot(self.W, X) + self.b
        return self.activator.activate(z)

    def get_cost(self, X, Y):
        return self.cost_object.cost(self.activate(X), Y)

    def propagate(self, X, y):
        m = X.shape[1]
        self.compute_cost(X, y)
        self.dz = self.cost_object.gradient_cost(self.a, y)
        self.dW = np.dot(self.dz, X.T) + self.regularizer.gradient(m, self.W)
        self.db = np.sum(self.dz, axis=1, keepdims=True)

        logger.debug("W={}, b={}".format(self.W, self.b))
        logger.debug("z[:,0]={}".format(self.z))
        logger.debug("a[:,0]={}".format(self.a))
        logger.debug("dW={}, db={}".format(self.dW, self.db))
        logger.debug("cost={}".format(self.cost))

    def fit(self, X, y, print_cost=False, print_num_epoch=1000):
        """
            Args:
                X -- data of shape (number of examples, number of features)
                y -- true "label" vector (containing 0 if non-cat, 1 if cat), of shape (number of examples, 1)
                print_cost --
        """
        assert(y.shape == (1, X.shape[1] ))
        assert(X.shape[0] == self.num_features)

        self.has_run_fit = True

        self.costs = []
        while self.iterator.iterate():
            self.propagate(X, y)
            self.update_parameters()

            if self.iterator.epoch_times % self.keep_cost_num_epoch == 0:
                self.costs.append(self.cost)
            if print_cost and self.iterator.epoch_times % print_num_epoch == 0:
                logger.info("Cost after epoch {}: {:.10f}".format(self.iterator.epoch_times, self.cost))
        self.compute_cost(X, y)
        if self.iterator.epoch_times % self.keep_cost_num_epoch == 0:
            self.costs.append(self.cost)
        if print_cost:
            logger.info("Final Cost after epoch {}: {:.10f}".format(self.iterator.epoch_times, self.cost))

    def update_parameters(self):
        self.optimizer.update_parameters(self)

    def plot_costs(self, title=None, xlabel=None, ylabel="cost", costs=None):
        if xlabel is None:
            xlabel = 'epochs (per ' + str(self.keep_cost_num_epoch) +')'
        if title is None:
            title = "Learning rate =" + str(self.optimizer.learning_rate)
        super().plot_costs(title, xlabel=xlabel, ylabel=ylabel, costs=costs)


class LogisticRegression(LinearModel):
    def __init__(self, num_features, activator=Sigmoid, regularizer=Regularizer(),
                 iterator=NumberIterator(100), optimizer=GradientOptimizer(0.001),
                 initializer=StaticWeightInitializer(0.01), keep_cost_num_epoch=1000,
                 cost_object=SigmoidCrossEntropy):
        LinearModel.__init__(self, num_features, activator=activator, regularizer=regularizer,
                             iterator=iterator, optimizer=optimizer,
                             initializer=initializer, keep_cost_num_epoch=keep_cost_num_epoch,
                             cost_object=cost_object)


class LinearRegression(LinearModel):
    def __init__(self, num_features, regularizer=Regularizer(),
                 iterator=NumberIterator(100), optimizer=GradientOptimizer(0.001),
                 initializer=WeightInitializer(), keep_cost_num_epoch=1000,
                 cost_object=MeanSquaredError
                 ):
        LinearModel.__init__(self, num_features, activator=Linear, regularizer=regularizer,
                             iterator=iterator, optimizer=optimizer,
                             initializer=initializer, keep_cost_num_epoch=keep_cost_num_epoch,
                             cost_object=cost_object)

    @classmethod
    def normal_equation(cls, X, y):
        X = add_intercept(X)
        theta = np.dot(y, np.dot(X.T, np.linalg.inv(np.dot(X, X.T)).T))
        b = theta[0:1, 0:1]
        w = theta[0:1, 1:]
        return w, b

if __name__ == "__main__":
    pass




