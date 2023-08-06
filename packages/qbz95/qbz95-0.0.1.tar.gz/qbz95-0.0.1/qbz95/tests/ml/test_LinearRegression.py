import unittest
from qbz95.ml.linear_model import *
from qbz95.ml.utils import *
from qbz95.ml.planar_utils import *
from qbz95.ml.predictor import Predictor

# logger.setLevel(level=logging.DEBUG)


class TestLinearRegression(unittest.TestCase):
    def test_compute_propagate(self):

        train_X, train_y = load_flat_dataset(data_path="../../../data/ex1data1.txt",)
        model = LinearRegression(num_features=train_X.shape[0],
                                 optimizer=GradientOptimizer(0.01),
                                 iterator=NumberIterator(50))
        model.propagate(train_X, train_y)

        print("train_X.shape={}".format(train_X.shape))
        print("train_y.shape={}".format(train_y.shape))
        print("cost={}".format(model.cost))

        np.testing.assert_almost_equal(model.cost, 32.07273388)

    def test_fit(self):

        train_X, train_y = load_flat_dataset(data_path="../../../data/ex1data1.txt",)
        model = LinearRegression(num_features=train_X.shape[0],
                                 optimizer=GradientOptimizer(0.01),
                                 iterator=NumberIterator(1500))
        model.fit(train_X, train_y, print_cost=True, print_num_epoch=100)
        print("cost={}".format(model.cost))
        print("W={}".format(model.W))
        print("b={}".format(model.b))

        np.testing.assert_array_almost_equal(model.W, [[1.166362350]])
        np.testing.assert_almost_equal(model.b, -3.630291439)
        np.testing.assert_almost_equal(model.cost, 4.483388257)

        predict1 = Predictor(model).predict(np.array([3.5]))
        print("predict1={}".format(predict1))
        np.testing.assert_almost_equal(predict1, 0.4519767868)

        predict2 = Predictor(model).predict(np.array([7]))
        print("predict2={}".format(predict2))
        np.testing.assert_almost_equal(predict2, 4.5342450129)

    def test_normal_equation(self):
        train_X, train_y = load_flat_dataset("../../../data/ex1data2.txt")

        W, b = LinearRegression.normal_equation(train_X, train_y)

        print("W={}".format(W))
        print("b={}".format(b))

        np.testing.assert_array_almost_equal(W, [[139.210674, -8738.019112]])
        np.testing.assert_almost_equal(b, 89597.909542798)

        train_X, mu, sigma = feature_normalize(train_X)
        print(train_X.shape)
        print("mu={}".format(mu))
        print("sigma={}".format(sigma))
        W, b = LinearRegression.normal_equation(train_X, train_y)
        print("W={}".format(W))
        print("b={}".format(b))

        #revert actual W, b
        b = b - np.dot(W, mu/sigma)
        W = W/sigma.T
        print("W={}".format(W))
        print("b={}".format(b))

        np.testing.assert_array_almost_equal(W, [[139.210674, -8738.019112]])
        np.testing.assert_almost_equal(b, 89597.909542798)


    def test_interate(self):
        train_X_orig, train_Y_orig, test_X_orig, test_Y_orig = load_sin_line_dataset(data_path="../../../data/sin_line.txt")

        print("train_X_orig.shape={}".format(train_X_orig.shape))
        print("train_Y_orig.shape={}".format(train_Y_orig.shape))
        print("test_X_orig.shape={}".format(test_X_orig.shape))
        print("test_Y_orig.shape={}".format(test_Y_orig.shape))

        train_X, train_Y, test_X, test_Y = (train_X_orig, train_Y_orig, test_X_orig, test_Y_orig)
        degree = 20
        train_X = map_feature(train_X, degree)
        test_X = map_feature(test_X, degree)

        print("train_X.shape={}".format(train_X.shape))
        print("train_Y.shape={}".format(train_Y.shape))
        print("test_X.shape={}".format(test_X.shape))
        print("test_Y.shape={}".format(test_Y.shape))

        model = LinearRegression(num_features=train_X.shape[0],
                                    regularizer=L2Regularizer(0), iterator=NumberIterator(100),
                                    optimizer=GradientOptimizer(0.5), initializer=WeightInitializer(),
                                    keep_cost_num_epoch=50)

        model.fit(train_X, train_Y, print_cost=True, print_num_epoch=50)

        print('train cost={}'.format(model.get_cost(train_X, train_Y)))
        print('test cost={}'.format(model.get_cost(test_X, test_Y)))
        print('W={}'.format(model.W))
        print('b={}'.format(model.b))
        predictor = Predictor(model)
        # predictor.plot_regression_curve(train_X_orig, train_Y_orig, X_model=train_X)



