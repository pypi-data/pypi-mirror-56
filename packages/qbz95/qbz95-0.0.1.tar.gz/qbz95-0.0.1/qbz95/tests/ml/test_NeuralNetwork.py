import unittest
from qbz95.ml.neural_network import *
from qbz95.ml.planar_utils import *
from qbz95.ml.predictor import *
from qbz95.tests.ml.testCases_v2 import *

logger.setLevel(level=logging.DEBUG)


class TestNeuralNetwork(unittest.TestCase):

    def test_layer_size(self):
        X_assess, Y_assess = layer_sizes_test_case()
        model = NeuralNetwork.build_3layers(X_assess, 4, Y_assess)
        print("The size of the input layer is: n_x = " + str(model.layers[0].num_neuron))
        print("The size of the hidden layer is: n_h = " + str(model.layers[1].num_neuron))
        print("The size of the output layer is: n_y = " + str(model.layers[2].num_neuron))
        np.testing.assert_equal(np.array([model.layers[0].num_neuron, model.layers[1].num_neuron, model.layers[2].num_neuron]),
                np.array([5, 4, 2]))

    def test_initialize_weights(self):
        np.random.seed(2)
        model = NeuralNetwork.build_layers([2, 4, 1])

        print("W1 = " + str(model.layers[1].W))
        print("b1 = " + str(model.layers[1].b))
        print("W2 = " + str(model.layers[2].W))
        print("b2 = " + str(model.layers[2].b))

        np.testing.assert_array_almost_equal(
            np.array([[-0.00416758, -0.00056267],
                      [-0.02136196, 0.01640271],
                      [-0.01793436, -0.00841747],
                      [0.00502881, -0.01245288]]),
            model.layers[1].W)

        np.testing.assert_array_almost_equal([[ 0.], [ 0.], [ 0.], [ 0.]], model.layers[1].b)
        np.testing.assert_array_almost_equal([[-0.01057952, -0.00909008,  0.00551454,  0.02292208]], model.layers[2].W)
        np.testing.assert_array_almost_equal([[ 0.]], model.layers[2].b)

    def test_forward_propagation(self):
        X_assess, Y_assess, parameters = forward_propagation_test_case()
        print(X_assess.shape)
        print(Y_assess.shape)
        print(parameters)

        np.random.seed(1)
        model = NeuralNetwork.build_3layers(X_assess, 4, Y_assess)
        model.layers[1].W = parameters['W1']
        model.layers[1].b = parameters['b1']
        model.layers[2].W = parameters['W2']
        model.layers[2].b = parameters['b2']
        model.forward_propagation(X_assess)

        mean = np.array([np.mean(model.layers[1].Z), np.mean(model.layers[1].A),
                         np.mean(model.layers[2].Z), np.mean(model.layers[2].A)])
        print(mean)
        np.testing.assert_array_almost_equal(mean,
                                             [0.262818640198, 0.091999045227, -1.30766601287, 0.212877681719])

    def test_compute_cost(self):
        X_assess, Y_assess, parameters = forward_propagation_test_case()
        model = NeuralNetwork.build_3layers(X_assess, 4, Y_assess)
        A2, Y_assess, parameters = compute_cost_test_case()
        print(A2)
        print(Y_assess)
        print(parameters)

        model.layers[2].W = parameters['W2']
        model.layers[2].b = parameters['b2']
        model.layers[2].A = A2
        cost = model.cost_object.cost(model.layers[2].A, Y_assess)
        print(cost)

        np.testing.assert_array_almost_equal(cost, 0.693058761039)

    def test_backward_propagation(self):
        parameters, cache, X_assess, Y_assess = backward_propagation_test_case()
        print(X_assess.shape)
        print(Y_assess.shape)
        print(parameters)

        np.random.seed(1)
        model = NeuralNetwork.build_3layers(X_assess, 4, Y_assess)
        model.layers[1].W = parameters['W1']
        model.layers[1].b = parameters['b1']
        model.layers[2].W = parameters['W2']
        model.layers[2].b = parameters['b2']
        model.layers[0].A = X_assess
        model.layers[1].Z = cache['Z1']
        model.layers[1].A = cache['A1']
        model.layers[2].Z = cache['Z2']
        model.layers[2].A = cache['A2']
        model.backward_propagation(Y_assess)

        print("dW1 = " + str(model.layers[1].dW))
        print("db1 = " + str(model.layers[1].db))
        print("dW2 = " + str(model.layers[2].dW))
        print("db2 = " + str(model.layers[2].db))
        np.testing.assert_array_almost_equal(model.layers[1].dW, [[0.00301023, -0.00747267],
                                                                  [0.00257968, -0.00641288],
                                                                  [-0.00156892, 0.003893],
                                                                  [-0.00652037, 0.01618243]])
        np.testing.assert_array_almost_equal(model.layers[1].db, [[0.00176201],
                                                                  [0.00150995],
                                                                  [-0.00091736],
                                                                  [-0.00381422]])
        np.testing.assert_array_almost_equal(model.layers[2].dW, [[0.00078841, 0.01765429, -0.00084166, -0.01022527]])
        np.testing.assert_array_almost_equal(model.layers[2].db, [[-0.16655712]])

    def test_fit(self):
        X_assess, Y_assess = nn_model_test_case()
        print(X_assess.shape)
        print(Y_assess.shape)

        np.random.seed(2)
        model = NeuralNetwork.build_3layers(X_assess, 4, Y_assess,
                                            iterator=NumberIterator(10000), learning_rate=1.2)
        model.fit(X_assess, Y_assess, print_cost=True)

        print("W1 = " + str(model.layers[1].W))
        print("b1 = " + str(model.layers[1].b))
        print("W2 = " + str(model.layers[2].W))
        print("b2 = " + str(model.layers[2].b))

        np.testing.assert_array_almost_equal([[-0.65848169, 1.21866811],
                                              [-0.76204273, 1.39377573],
                                              [0.5792005, -1.10397703],
                                              [0.76773391, -1.41477129]], model.layers[1].W)
        np.testing.assert_array_almost_equal([[0.287592], [0.3511264], [-0.2431246], [-0.35772805]], model.layers[1].b)
        np.testing.assert_array_almost_equal([[-2.45566237, -3.27042274 , 2.00784958,  3.36773273]], model.layers[2].W)
        np.testing.assert_array_almost_equal([[ 0.20459656]], model.layers[2].b)


    def test_compute_cost_with_regularization(self):
        A3, Y_assess, parameters = compute_cost_with_regularization_test_case()

        model = NeuralNetwork.build_layers([3, 2, 3, 1], regularizer=L2Regularizer(0.1))
        model.layers[1].W = parameters["W1"]
        model.layers[2].W = parameters["W2"]
        model.layers[3].W = parameters["W3"]
        model.layers[3].A = A3
        model.compute_cost(Y_assess)

        print("cost = " + str(model.cost))
        np.testing.assert_almost_equal(1.78648594516, model.cost)

    def test_backward_propagation_with_regularization(self):
        X_assess, Y_assess, cache = backward_propagation_with_regularization_test_case()
        (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3) = cache


        model = NeuralNetwork.build_layers(
            [X_assess.shape[0], Z1.shape[0], Z2.shape[0], Z3.shape[0]],
            activators=[Relu, Relu, Sigmoid],
            regularizer=L2Regularizer(0.7))
        model.layers[0].A = X_assess
        model.layers[1].W = W1
        model.layers[1].b = b1
        model.layers[1].A = A1
        model.layers[1].Z = Z1
        model.layers[2].W = W2
        model.layers[2].b = b2
        model.layers[2].A = A2
        model.layers[2].Z = Z2
        model.layers[3].W = W3
        model.layers[3].b = b3
        model.layers[3].A = A3
        model.layers[3].Z = Z3

        model.backward_propagation(Y_assess)

        print("dW1 = " + str(model.layers[1].dW))
        print("dW2 = " + str(model.layers[2].dW))
        print("dW3 = " + str(model.layers[3].dW))
        # np.testing.assert_almost_equal(1.78648594516, model.cost)
        np.testing.assert_array_almost_equal([[-0.25604646,  0.12298827, - 0.28297129],
                                              [-0.17706303,  0.34536094, - 0.4410571]], model.layers[1].dW)

        np.testing.assert_array_almost_equal([[0.79276486,  0.85133918],
                                              [-0.0957219, - 0.01720463],
                                              [-0.13100772, - 0.03750433]], model.layers[2].dW)
        np.testing.assert_array_almost_equal([[-1.77691347, - 0.11832879, - 0.09397446]], model.layers[3].dW)

    def test_backward_propagation_with_dropout(self):
        X_assess, parameters = forward_propagation_with_dropout_test_case()
        np.random.seed(1)
        model = NeuralNetwork.build_layers(
            [X_assess.shape[0], 2, 3, 1],
            activators=[Relu, Relu, Sigmoid],
            regularizer=Regularizer(),
            keep_prob = 0.7
        )
        model.layers[1].W = parameters['W1']
        model.layers[1].b = parameters['b1']
        model.layers[2].W = parameters['W2']
        model.layers[2].b = parameters['b2']
        model.layers[3].W = parameters['W3']
        model.layers[3].b = parameters['b3']
        model.layers[0].A = X_assess

        model.forward_propagation(X_assess)
        print("A3 = " + str(model.output_layer.A))
        np.testing.assert_array_almost_equal([[0.36974721, 0.00305176, 0.04565099, 0.49683389, 0.36974721]], model.output_layer.A)

    def test_backward_propagation_with_dropout(self):
        X_assess, Y_assess, cache = backward_propagation_with_dropout_test_case()
        (Z1, D1, A1, W1, b1, Z2, D2, A2, W2, b2, Z3, A3, W3, b3) = cache

        model = NeuralNetwork.build_layers(
            [X_assess.shape[0], Z1.shape[0], Z2.shape[0], Z3.shape[0]],
            activators=[Relu, Relu, Sigmoid],
            regularizer=Regularizer(),
            keep_prob=0.8)
        model.layers[0].A = X_assess
        model.layers[1].W = W1
        model.layers[1].b = b1
        model.layers[1].A = A1
        model.layers[1].D = D1
        model.layers[1].Z = Z1
        model.layers[2].W = W2
        model.layers[2].b = b2
        model.layers[2].A = A2
        model.layers[2].D = D2
        model.layers[2].Z = Z2
        model.layers[3].W = W3
        model.layers[3].b = b3
        model.layers[3].A = A3
        model.layers[3].Z = Z3

        model.backward_propagation(Y_assess)

        print("dZ1 = " + str(model.layers[1].dZ))
        print("dZ2 = " + str(model.layers[2].dZ))
        print("dZ3 = " + str(model.layers[3].dZ))

        np.testing.assert_array_almost_equal([[0.00019884,  0.00028657,  0.00012138],
                                              [0.00035647,  0.00051375,  0.00021761]], model.layers[1].dW)

        np.testing.assert_array_almost_equal([[-0.00256518, - 0.0009476],
                                              [0.,        0.],
                                              [0.,        0.]], model.layers[2].dW)
        np.testing.assert_array_almost_equal([[-0.06951191,  0.,         0.]], model.layers[3].dW)


    def test_gradient_check(self):
        X, Y, parameters = gradient_check_n_test_case()

        model = NeuralNetwork.build_layers(
            [X.shape[0], 5, 3, Y.shape[0]],
            activators=[Relu, Relu, Sigmoid],
            regularizer=L2Regularizer(10),
            keep_prob=0.65)

        model.layers[1].W = parameters['W1']
        model.layers[1].b = parameters['b1']
        model.layers[2].W = parameters['W2']
        model.layers[2].b = parameters['b2']
        model.layers[3].W = parameters['W3']
        model.layers[3].b = parameters['b3']
        model.layers[0].A = X

        return model.gradient_check(X, Y)

    def test_adam(self):
        parameters, grads, v, s = update_parameters_with_adam_test_case()

        model = NeuralNetwork.build(
            [3, 2, 3],
            activators=[Relu, Sigmoid],
            optimizer=AdamOptimizer(learning_rate = 0.01, beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8))
        model.layers[1].W = parameters["W1"]
        model.layers[1].b = parameters["b1"]
        model.layers[1].t = 1
        model.layers[2].W = parameters["W2"]
        model.layers[2].b = parameters["b2"]
        model.layers[2].t = 1

        model.layers[1].dW = grads["dW1"]
        model.layers[1].db = grads["db1"]
        model.layers[2].dW = grads["dW2"]
        model.layers[2].db = grads["db2"]

        model.update_parameters()

        print("W1 = " + str(model.layers[1].W))
        print("b1 = " + str(model.layers[1].b))
        print("W2 = " + str(model.layers[2].W))
        print("b2 = " + str(model.layers[2].b))
        print("v[\"dW1\"] = " + str(model.layers[1].vW))
        print("v[\"db1\"] = " + str(model.layers[1].vb))
        print("v[\"dW2\"] = " + str(model.layers[2].vW))
        print("v[\"db2\"] = " + str(model.layers[2].vb))
        print("s[\"dW1\"] = " + str(model.layers[1].sW))
        print("s[\"db1\"] = " + str(model.layers[1].sb))
        print("s[\"dW2\"] = " + str(model.layers[2].sW))
        print("s[\"db2\"] = " + str(model.layers[2].sb))

        np.testing.assert_array_almost_equal([[ 1.63178673, -0.61919778, -0.53561312],
                                              [-1.08040999, 0.85796626, -2.29409733]], model.layers[1].W)
        np.testing.assert_array_almost_equal([[ 1.75225313], [-0.75376553]], model.layers[1].b)
        np.testing.assert_array_almost_equal([[ 0.32648046, -0.25681174, 1.46954931],
                                              [-2.05269934, -0.31497584, -0.37661299],
                                              [ 1.14121081, -1.09245036, -0.16498684]], model.layers[2].W)
        np.testing.assert_array_almost_equal([[-0.88529978], [ 0.03477238], [ 0.57537385]], model.layers[2].b)
        np.testing.assert_array_almost_equal([[-0.11006192, 0.11447237, 0.09015907],
                                              [ 0.05024943, 0.09008559, -0.06837279]], model.layers[1].vW)
        np.testing.assert_array_almost_equal([[-0.01228902], [-0.09357694]], model.layers[1].vb)
        np.testing.assert_array_almost_equal([[-0.02678881, 0.05303555, -0.06916608],
                                              [-0.03967535, -0.06871727, -0.08452056],
                                              [-0.06712461, -0.00126646, -0.11173103]], model.layers[2].vW)
        np.testing.assert_array_almost_equal([[ 0.02344157], [ 0.16598022], [ 0.07420442]], model.layers[2].vb)
        np.testing.assert_array_almost_equal([[ 0.00121136, 0.00131039, 0.00081287], [ 0.0002525, 0.00081154, 0.00046748]], model.layers[1].sW)
        np.testing.assert_array_almost_equal([[ 1.51020075e-05], [ 8.75664434e-04]], model.layers[1].sb)
        np.testing.assert_array_almost_equal([[ 7.17640232e-05, 2.81276921e-04, 4.78394595e-04],
                                              [ 1.57413361e-04, 4.72206320e-04, 7.14372576e-04],
                                              [ 4.50571368e-04, 1.60392066e-07, 1.24838242e-03]], model.layers[2].sW)
        np.testing.assert_array_almost_equal([[ 5.49507194e-05], [ 2.75494327e-03], [ 5.50629536e-04]], model.layers[2].sb)

    def test_momentum(self):
        parameters, grads, v = update_parameters_with_momentum_test_case()

        model = NeuralNetwork.build(
            [3, 2, 3],
            activators=[Relu, Sigmoid],
            optimizer=MomentumOptimizer(learning_rate = 0.01, beta = 0.9))
        model.layers[1].W = parameters["W1"]
        model.layers[1].b = parameters["b1"]
        model.layers[2].W = parameters["W2"]
        model.layers[2].b = parameters["b2"]

        model.layers[1].dW = grads["dW1"]
        model.layers[1].db = grads["db1"]
        model.layers[2].dW = grads["dW2"]
        model.layers[2].db = grads["db2"]

        model.update_parameters()

        print("W1 = " + str(model.layers[1].W))
        print("b1 = " + str(model.layers[1].b))
        print("W2 = " + str(model.layers[2].W))
        print("b2 = " + str(model.layers[2].b))
        print("v[\"dW1\"] = " + str(model.layers[1].vW))
        print("v[\"db1\"] = " + str(model.layers[1].vb))
        print("v[\"dW2\"] = " + str(model.layers[2].vW))
        print("v[\"db2\"] = " + str(model.layers[2].vb))

        np.testing.assert_array_almost_equal([[ 1.62544598, -0.61290114, -0.52907334],
                                              [-1.07347112, 0.86450677, -2.30085497]], model.layers[1].W)
        np.testing.assert_array_almost_equal([[ 1.74493465], [-0.76027113]], model.layers[1].b)
        np.testing.assert_array_almost_equal([[ 0.31930698, -0.24990073, 1.4627996 ],
                                              [-2.05974396, -0.32173003, -0.38320915],
                                              [ 1.13444069, -1.0998786, -0.1713109 ]], model.layers[2].W)
        np.testing.assert_array_almost_equal([[-0.87809283], [ 0.04055394], [ 0.58207317]], model.layers[2].b)
        np.testing.assert_array_almost_equal([[-0.11006192, 0.11447237, 0.09015907],
                                              [ 0.05024943, 0.09008559, -0.06837279]], model.layers[1].vW)
        np.testing.assert_array_almost_equal([[-0.01228902], [-0.09357694]], model.layers[1].vb)
        np.testing.assert_array_almost_equal([[-0.02678881, 0.05303555, -0.06916608],
                                              [-0.03967535, -0.06871727, -0.08452056],
                                              [-0.06712461, -0.00126646, -0.11173103]], model.layers[2].vW)
        np.testing.assert_array_almost_equal([[ 0.02344157], [ 0.16598022], [ 0.07420442]], model.layers[2].vb)


    def test_interate(self):
        train_X_orig, train_Y_orig, test_X_orig, test_Y_orig = load_petal_dataset()
        print("train_X_orig.shape={}".format(train_X_orig.shape))
        print("train_Y_orig.shape={}".format(train_Y_orig.shape))
        print("test_X_orig.shape={}".format(test_X_orig.shape))
        print("test_Y_orig.shape={}".format(test_Y_orig.shape))

        learning_rate = 0.025

        # batch
        epoch_times = 1000
        mini_batch = 100
        print_num_epoch = 50
        keep_cost_num_epoch = 50

        # initialize
        static_weight_scale = 10

        # regularize
        alpha = 0.01
        keep_prob = 1

        # optimize
        beta = 0.9
        beta1 = 0.9
        beta2 = 0.99
        epsilon = 1e-8

        train_X, train_Y, test_X, test_Y = (train_X_orig, train_Y_orig, test_X_orig, test_Y_orig)
        # train_X, train_Y, test_X, test_Y = load_petal_dataset(num_example=2000) #?????????????
        num_neurons = [train_X.shape[0], 16, 8, 1]
        activators = [Relu, Relu, Sigmoid]

        model = NeuralNetwork.build(
            num_neurons=num_neurons,
            activators=activators,
            iterator=NumberIterator(epoch_times),
            initializer=HeWeightInitializer(),
            optimizer=AdamOptimizer(learning_rate=learning_rate, beta1=beta1, beta2=beta2, epsilon=epsilon),
            keep_cost_num_epoch=keep_cost_num_epoch,
            mini_batch=mini_batch,
            regularizer=L2Regularizer(alpha),
            keep_prob=keep_prob
        )

        model.fit(train_X, train_Y, print_cost=False, print_num_epoch=print_num_epoch)
        # model.plot_costs()

        predictor = ClassificationPredictor(model=model)
        predictor.print_metrics(train_X, train_Y, test_X=test_X, test_Y=test_Y)

        predictor = ProbabilityPredictor(model=model)
        predictor.print_metrics(train_X, train_Y, test_X=test_X, test_Y=test_Y)

