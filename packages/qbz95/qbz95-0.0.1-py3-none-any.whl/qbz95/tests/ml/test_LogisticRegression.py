import unittest
from qbz95.ml.linear_model import *
from qbz95.ml.utils import *
from qbz95.ml.planar_utils import *
from qbz95.ml.predictor import ClassificationPredictor

# logger.setLevel(level=logging.DEBUG)


class TestLogisticRegression(unittest.TestCase):
    def test_sigmoid(self):
        s = sigmoid(np.array([0, 2]))
        print("sigmoid([0, 2]) = " + str(s))
        np.testing.assert_array_almost_equal(s, np.array([0.5, 0.88079708]))

    def test_initialize_image(self):
        train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes = \
            load_image_data(train_data_path='../../../data/train_catvnoncat.h5', test_data_path='../../../data/test_catvnoncat.h5')
        train_set_x, train_set_y = initialize_image_data(train_set_x_orig, train_set_y_orig)
        test_set_x, test_set_y = initialize_image_data(test_set_x_orig, test_set_y_orig)

        print("train_set_x shape: " + str(train_set_x.shape))
        print("train_set_y shape: " + str(train_set_y.shape))
        print("test_set_x shape: " + str(test_set_x.shape))
        print("test_set_y shape: " + str(test_set_y.shape))
        print("sanity check after reshaping: " + str(train_set_x[0:6, 0:4]))
        print("sanity check after reshaping: " + str(train_set_x[0:5, 0] * 255))

        np.testing.assert_array_almost_equal(train_set_x[0:5, 0:4],
                                             np.array([[0.06666667,  0.12156863,  0.21960784,  0.08627451,  0.12941176],
                                                       [0.76862745,  0.75294118,  0.74509804,  0.75686275,  0.72941176],
                                                       [0.32156863,  0.27843137,  0.26666667,  0.34901961,  0.3254902],
                                                       [0.00392157,  0.08627451,  0.00784314,  0.00392157,  0.05490196]]).T)

        np.testing.assert_array_almost_equal(train_set_x[0:5, 0] * 255, [17.,  31.,  56.,  22. , 33.])

    def test_propagate(self):
        # check if model.propagate is correct
        X = np.array([[1., 2., -1.], [3., 4., -3.2]])
        y = np.array([[1], [0], [1]]).T
        W = np.array([[1.], [2.]]).T
        b = 2
        print("X = " + str(X))
        print("y = " + str(y))
        print("W = " + str(W))
        print("b = " + str(b))

        model = LogisticRegression(num_features=X.shape[0], optimizer=GradientOptimizer(0.009),
                                   iterator=NumberIterator(100))
        model.W = W
        model.b = b

        model.propagate(X, y)
        print("dW = " + str(model.dW))
        print("db = " + str(model.db))
        print("cost = " + str(model.cost))

        assert (y.shape == (1, X.shape[1] ))
        np.testing.assert_array_almost_equal(model.dW, np.array([[9.98456015e-01], [2.39507239e+00]]).T)
        np.testing.assert_array_almost_equal(model.db, 1.45557814e-03)
        np.testing.assert_array_almost_equal(model.cost, 5.80154532)

        # check if model.train is correct
        model.fit(X, y, print_cost=True, print_num_epoch=10)

        print("W = " + str(model.W))
        print("b = " + str(model.b))
        print("dW = " + str(model.dW))
        print("db = " + str(model.b))
        np.testing.assert_array_almost_equal(model.W, np.array([[0.19033591], [0.12259159]]).T)
        np.testing.assert_array_almost_equal(model.b, 1.92535983008)
        np.testing.assert_array_almost_equal(model.dW, np.array([[0.67752042], [1.41625495]]).T)
        np.testing.assert_array_almost_equal(model.db, 0.219194504541)
