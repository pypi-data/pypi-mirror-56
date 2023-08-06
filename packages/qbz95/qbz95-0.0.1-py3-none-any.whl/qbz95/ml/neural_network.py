from qbz95.ml.planar_utils import load_planar_dataset
from qbz95.ml.model import Model
from qbz95.ml.utils import *



class NeuronLayer(object):
    def __init__(self, num_neuron, num_weights):
        self.num_neuron = num_neuron
        self.num_weights = num_weights

    def forward_propagation(self, A):
        pass

    def backward_propagation(self, pre_layer, next_layer):
        pass


class InputLayer(NeuronLayer):
    def __init__(self, feature_num):
        NeuronLayer.__init__(self, feature_num, 0)
        self.A = None

    def forward_propagation(self, A, use_keep_prob=True):
        assert (A.shape[0] == self.num_neuron)
        self.A = A

    def print_layer(self):
        if self.A is not None:
            logger.info("A=" + str(self.A))


class HiddenLayer(NeuronLayer):

    def __init__(self, num_neuron, num_weights, activator=Sigmoid,
                 initializer=StaticWeightInitializer(0.01), regularizer=Regularizer(),
                 keep_prob=1, optimizer = GradientOptimizer(0.01)):
        assert(keep_prob <= 1 and keep_prob > 0)
        NeuronLayer.__init__(self, num_neuron, num_weights)
        self.activator = activator
        self.W, self.b = initializer.initial_weights(num_neuron, num_weights)
        self.regularizer = regularizer
        self.keep_prob = keep_prob
        self.optimizer = optimizer
        self.A = None
        self.Z = None
        self.D = None
        self.dA = None
        self.dZ = None
        self.dW = None
        self.db = None
        self.t = 0
        self.has_initialize_optimizer = False

    def print_layer(self):
        logger.info("W=" + str(self.W))
        logger.info("b=" + str(self.b))
        if self.D is not None:
            logger.info("D=" + str(self.D))
        if self.Z is not None:
            logger.info("Z=" + str(self.Z))
        if self.A is not None:
            logger.info("A=" + str(self.A))

    def regularize(self, m):
        return self.regularizer.regularize(m, self.W)

    def forward_propagation(self, A, use_keep_prob=True):
        assert(A.shape[0] == self.num_weights)
        m = A.shape[1]
        self.Z = np.dot(self.W, A) + self.b
        self.A = self.activator.activate(self.Z)
        if use_keep_prob and self.keep_prob < 1:
            D = np.random.rand(self.A.shape[0], self.A.shape[1])
            # if self.D is not None:
            #     np.testing.assert_array_equal(np.int64(D < self.keep_prob), self.D)
            #     logger.info("D always is same after every epoch")
            self.D = np.int64(D < self.keep_prob)
            self.A = self.A * self.D/self.keep_prob

    def backward_propagation(self, pre_layer, next_layer):
        m = self.Z.shape[1]
        # self.dZ = self.activator.gradient_layer(self.Z, next_layer)
        self.dA = np.dot(next_layer.W.T, next_layer.dZ)
        self.dZ = np.multiply(self.dA, self.activator.gradient(self.Z))
        if self.keep_prob < 1 and self.D is not None:
            self.dZ = self.dZ * self.D/self.keep_prob
        self.dW = np.dot(self.dZ, pre_layer.A.T) + self.regularizer.gradient(m, self.W)
        self.db = np.sum(self.dZ, axis=1, keepdims=True)

    def update_parameters(self):
        if not self.has_initialize_optimizer:
            self.optimizer.initialize(self)
            self.has_initialize_optimizer = True
        self.optimizer.update_parameters(self)


class OutputLayer(HiddenLayer):

    def __init__(self, num_neuron, num_weights, activator=Sigmoid,
                 initializer=StaticWeightInitializer(0.01), regularizer=Regularizer(),
                 optimizer=GradientOptimizer(0.01)):
        HiddenLayer.__init__(self, num_neuron, num_weights, activator,
                    initializer=initializer, regularizer=regularizer,
                    keep_prob=1, optimizer=optimizer)
        # self.cost = None

    # def compute_cost(self, Y):
    #     self.cost = self.activator.compute_cost(self.A, Y)

    def backward_propagation(self, pre_layer, dZ):
        m = dZ.shape[1]
        self.dZ = dZ #self.activator.gradient_cost(self.A, Y)
        self.dW = np.dot(self.dZ, pre_layer.A.T) + self.regularizer.gradient(m, self.W)
        self.db = np.sum(self.dZ, axis=1, keepdims=True)


class NeuralNetwork(Model):

    def __init__(self,
                 layers, iterator=NumberIterator(100),
                 keep_cost_num_epoch=1000,
                 mini_batch=0,
                 cost_object=SigmoidCrossEntropy
                 ):
        Model.__init__(self)
        assert(len(layers) >= 2)
        assert(mini_batch >= 0)
        self.layers = layers
        self.num_layer = len(layers)
        self.input_layer = self.layers[0]
        self.output_layer = self.layers[self.num_layer-1]
        self.iterator = iterator
        self.keep_cost_num_epoch = keep_cost_num_epoch
        self.has_run_fit = False
        self.mini_batch = mini_batch
        self.costs=[]
        self.cost=None
        self.cost_object = cost_object
        self.debug_parameters("initialize")

    @classmethod
    def build_3layers(cls, X, num_hidden_neuron, Y, iterator=NumberIterator(100), learning_rate=0.001,
                      initializer=StaticWeightInitializer(0.01), regularizer=Regularizer(),
                      cost_object=SigmoidCrossEntropy):
        input = InputLayer(X.shape[0])
        hidden = HiddenLayer(num_hidden_neuron, input.num_neuron, activator=Tanh,
                             initializer=initializer, regularizer=regularizer,
                             optimizer=GradientOptimizer(learning_rate)
                             )
        output = OutputLayer(Y.shape[0], hidden.num_neuron, activator=Sigmoid,
                             initializer=initializer, regularizer=regularizer,
                             optimizer=GradientOptimizer(learning_rate))
        layers = [input, hidden, output]
        model = NeuralNetwork(layers, iterator=iterator, cost_object=cost_object)
        return model

    @classmethod
    def build(cls, num_neurons, activators=[Sigmoid], iterator=NumberIterator(100),
                      optimizer=GradientOptimizer(0.001), initializer=StaticWeightInitializer(0.01),
                      regularizer=Regularizer(), keep_prob=1, mini_batch=0,
                      keep_cost_num_epoch=1000, initialize_seed = 3, cost_object=SigmoidCrossEntropy):
        layers = []
        len_layer = len(num_neurons)
        len_activator = len(activators)
        assert (len_activator == 1 or len_activator == len_layer - 1)
        if initialize_seed > 0: np.random.seed(initialize_seed)
        for i in range(len_layer):

            if i == 0:
                layers.append(InputLayer(num_neurons[i]))
            else:
                if len(activators) == 1:
                    activator = activators[0]
                else:
                    activator = activators[i - 1]
                if i == len_layer - 1:
                    layers.append(OutputLayer(num_neurons[i], layers[i - 1].num_neuron, activator=activator,
                                              initializer=initializer, regularizer=regularizer,
                                              optimizer=optimizer))
                else:
                    layers.append(HiddenLayer(num_neurons[i], layers[i - 1].num_neuron, activator=activator,
                                              initializer=initializer, regularizer=regularizer,
                                              keep_prob=keep_prob, optimizer=optimizer))

        model = NeuralNetwork(layers, iterator=iterator, keep_cost_num_epoch=keep_cost_num_epoch,
                              mini_batch=mini_batch, cost_object=cost_object)
        return model

    @classmethod
    def build_layers(cls, num_neurons, activators=[Sigmoid], iterator=NumberIterator(100), learning_rate=0.001,
                     initializer=StaticWeightInitializer(0.01), regularizer=Regularizer(), keep_prob = 1, mini_batch=0,
                     keep_cost_num_epoch=1000):
        layers = []
        len_layer = len(num_neurons)
        len_activator = len(activators)
        assert(len_activator==1 or len_activator==len_layer-1)
        for i in range(len_layer):

            if i == 0:
                layers.append(InputLayer(num_neurons[i]))
            else:
                if len(activators) == 1:
                    activator = activators[0]
                else:
                    activator = activators[i-1]
                if i == len_layer-1:
                    layers.append(OutputLayer(num_neurons[i], layers[i-1].num_neuron, activator=activator,
                                              initializer=initializer, regularizer=regularizer,
                                              optimizer=GradientOptimizer(learning_rate)))
                else:
                    layers.append(HiddenLayer(num_neurons[i], layers[i-1].num_neuron, activator=activator,
                                              initializer=initializer, regularizer=regularizer,
                                              keep_prob=keep_prob, optimizer=GradientOptimizer(learning_rate)))

        model = NeuralNetwork(layers, iterator=iterator, keep_cost_num_epoch=keep_cost_num_epoch, mini_batch=mini_batch)
        return model

    def debug_double_line(self, title=""):
        if self.iterator.epoch_times < 1:
            logger.debug("======================{}======================".format(title))

    def debug_line(self, title=""):
        if self.iterator.epoch_times < 1:
            logger.debug("----------------------{}----------------------".format(title))

    def info_line(self, title=""):
        logger.info("----------------------{}----------------------".format(title))

    def debug_parameters(self, title):
        if logger.level == logging.DEBUG and self.iterator.epoch_times < 1:
            for i in range(1, len(self.layers)):
                self.debug_line("layer {} - {} - parameters".format(i, title))
                logger.debug("W=" + str(self.layers[i].W))
                logger.debug("b=" + str(self.layers[i].b))

    def debug_gradient(self, title):
        if logger.level == logging.DEBUG and self.iterator.epoch_times < 1:
            for i in range(1, len(self.layers)):
                self.debug_line("layer {} - {} - gradient".format(i, title))
                if self.layers[i].dA is not None:
                    logger.debug("dA[:, 0]=" + str(self.layers[i].dA[:, 0]))
                logger.debug("dZ[:, 0]=" + str(self.layers[i].dZ[:, 0]))
                logger.debug("dW=" + str(self.layers[i].dW))
                logger.debug("db=" + str(self.layers[i].db))

    def debug_output(self, title=""):
        if logger.level == logging.DEBUG and self.iterator.epoch_times < 1:
            for i in range(1, len(self.layers)):
                self.debug_line("layer {} - {} - output".format(i, title))
                logger.debug("Z[:, 0]=" + str(self.layers[i].Z[:, 0]))
                logger.debug("A[:, 0]=" + str(self.layers[i].A[:, 0]))

    def forward_propagation(self, X, use_keep_prob=True, keep_prob_seed=1):
        if use_keep_prob and keep_prob_seed > 0:
            np.random.seed(keep_prob_seed)   # mainly used for dropout matrix.
        for i in range(self.num_layer):
            if i == 0:
                self.layers[i].forward_propagation(X, use_keep_prob)
            else:
                self.layers[i].forward_propagation(self.layers[i-1].A, use_keep_prob)

    def backward_propagation(self, Y):
        i = self.num_layer - 2
        dZ = self.cost_object.gradient_cost(self.output_layer.A, Y)
        self.output_layer.backward_propagation(self.layers[i], dZ)
        while i > 0:
            pre_layer = self.layers[i - 1]
            next_layer = self.layers[i + 1]
            self.layers[i].backward_propagation(pre_layer, next_layer)
            i = i - 1

    def update_parameters(self):
        for i in range(1, self.num_layer):
            self.layers[i].update_parameters()

    def compute_cost(self, Y):
        regularize_cost = 0
        m = Y.shape[1]
        for i in range(1, self.num_layer):
            regularize_cost = regularize_cost + self.layers[i].regularize(m)
        self.cost = self.cost_object.cost(self.output_layer.A, Y) + regularize_cost

    def get_cost(self, X, Y):
        self.activate(X)
        return self.cost_object.cost(self.output_layer.A, Y)

    def get_batch(self, m):
        batch = m if self.mini_batch == 0 or self.mini_batch > m else self.mini_batch
        return batch

    def shuffle_data(self, batch, X, Y, shuffle_seed):
        if shuffle_seed > 0:
            np.random.seed(shuffle_seed)
        m = X.shape[1]
        if batch < m:
            permutation = list(np.random.permutation(m))
            shuffled_X = X[:, permutation]
            shuffled_Y = Y[:, permutation].reshape((1, m))
        else:
            shuffled_X = X
            shuffled_Y = Y
        return shuffled_X, shuffled_Y

    def fit(self, X, Y, print_cost=False, print_num_epoch=1000, shuffle_seed=11):
        self.has_run_fit = True
        self.costs = []

        m = X.shape[1]
        batch = self.get_batch(m)

        while self.iterator.iterate():
            shuffled_X, shuffled_Y = self.shuffle_data(batch, X, Y, shuffle_seed)
            shuffle_seed = shuffle_seed + 1
            start = 0
            while start < m:
                end = start + batch
                end = end if end<=m else m
                self.debug_double_line("start={}, end={}, m={}".format(start, end, m))
                X_last = shuffled_X[:, start:end]
                Y_last = shuffled_Y[:, start:end]
                self.fit_batch(X_last, Y_last)
                start = end
            if self.iterator.epoch_times % self.keep_cost_num_epoch == 0:
                self.costs.append(self.cost)
            if print_cost and self.iterator.epoch_times % print_num_epoch == 0:
                logger.info("Cost after epoch {}: {:.10f}".format(self.iterator.epoch_times, self.cost))

        self.forward_propagation(X_last)
        self.compute_cost(Y_last)
        if self.iterator.epoch_times % self.keep_cost_num_epoch == 0:
            self.costs.append(self.cost)
        if print_cost:
            logger.info("Final Cost after epoch {}: {:.10f}".format(self.iterator.epoch_times, self.cost))

    def fit_batch(self, X, Y):
        self.forward_propagation(X)
        self.debug_output("forward propagation")
        self.compute_cost(Y)
        self.backward_propagation(Y)
        self.debug_gradient("back propagation")
        self.update_parameters()
        self.debug_parameters("update_parameters")

        self.debug_line("cost={}".format(self.cost))

    def print_layers(self):
        for i in range(1, self.num_layer):
            NeuralNetwork.print_layer_line(i)
            self.layers[i].print_layer()

    def activate(self, X):
        """
        predict. ignore dropout when predict.
        :param X:
        :return:
        """
        assert (self.has_run_fit)
        self.forward_propagation(X, use_keep_prob=False)
        return self.output_layer.A


    def plot_costs(self, title=None, xlabel=None, ylabel="cost", costs=None):
        if xlabel is None:
            xlabel = 'epochs (per ' + str(self.keep_cost_num_epoch) +')'
        if title is None:
            title = "Learning rate =" + str(self.output_layer.optimizer.learning_rate)
        super().plot_costs(title, xlabel=xlabel, ylabel=ylabel, costs=costs)

    def gradient_check(self, X, Y, epsilon=1e-7):
        grad = []
        grad_approx = []
        self.forward_propagation(X)
        self.backward_propagation(Y)
        for i in range(1, self.num_layer):
            W = self.layers[i].W
            b = self.layers[i].b
            for j in range(self.layers[i].num_neuron):
                for k in range(self.layers[i].num_weights):
                    self.layers[i].W = np.copy(W)
                    self.layers[i].W[j, k] = self.layers[i].W[j, k] + epsilon
                    self.forward_propagation(X)
                    self.compute_cost(Y)
                    cost_plus = self.cost

                    self.layers[i].W = np.copy(W)
                    self.layers[i].W[j, k] = self.layers[i].W[j, k] - epsilon
                    self.forward_propagation(X)
                    self.compute_cost(Y)
                    cost_minus = self.cost

                    grad_approx.append((cost_plus - cost_minus) / 2 / epsilon)
                    grad.append(self.layers[i].dW[j, k])

                self.layers[i].W = W

                self.layers[i].b = np.copy(b)
                self.layers[i].b[j, 0] = self.layers[i].b[j, 0] + epsilon
                self.forward_propagation(X)
                self.compute_cost(Y)
                cost_plus = self.cost

                self.layers[i].b = np.copy(b)
                self.layers[i].b[j, 0] = self.layers[i].b[j, 0] - epsilon
                self.forward_propagation(X)
                self.compute_cost(Y)
                cost_minus = self.cost

                grad_approx.append((cost_plus - cost_minus) / 2 / epsilon)
                grad.append(self.layers[i].db[j, 0])

            self.layers[i].b = b
        grad_approx = np.asarray(grad_approx)
        grad = np.asarray(grad)
        numerator = np.sum(np.power(grad_approx - grad, 2))
        denominator = np.sum(np.power(grad_approx, 2)) + np.sum(np.power(grad, 2))
        difference = numerator / denominator

        if difference > 2e-7:
            logger.info("There is a mistake in the backward propagation! difference = " + str(difference) )
        else:
            logger.info("Your backward propagation works perfectly fine! difference = " + str(difference) )
        assert(difference <= 2e-7)
        return difference


if __name__ == "__main__":
    from qbz95.tests.ml.testCases_v2 import *
    X, Y = load_planar_dataset()
    logger.setLevel(logging.DEBUG)

    logger.info("logger.level={}".format(logger.level))
    logger.info(X.shape)
    logger.info(Y.shape)

    input_layer = InputLayer(X.shape[0])
    hidden_layer = HiddenLayer(5, input_layer.num_neuron, activator=Tanh)
    output_layer = OutputLayer(1, hidden_layer.num_neuron, activator=Sigmoid)
    layers = [input_layer, hidden_layer, output_layer]
    model = NeuralNetwork(layers, iterator=NumberIterator(100))
    model.debug_parameters("abc")
    X_assess, Y_assess, parameters = forward_propagation_test_case()
    logger.info((X_assess, Y_assess, parameters ))