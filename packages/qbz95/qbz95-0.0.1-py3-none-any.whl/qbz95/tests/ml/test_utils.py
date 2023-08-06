import unittest
from qbz95.ml.utils import *
from qbz95.ml.planar_utils import *

logger.setLevel(level=logging.DEBUG)


class TestUtils(unittest.TestCase):

    def test_map_feature(self):
        X = np.arange(0, 8).reshape(2, 4)
        print("X={}".format(X))
        X1 = map_feature(X, 1)
        X2 = map_feature(X, 2)
        X3 = map_feature(X, 3)
        print("X1={}".format(X1))
        print("X2={}".format(X2))
        print("X3={}".format(X3))

        np.testing.assert_array_almost_equal(X3, [[   0.,   1.,   2.,   3.],
                                                  [   4.,   5.,   6.,   7.],
                                                  [   0.,   1.,   4.,   9.],
                                                  [   0.,   5.,  12.,  21.],
                                                  [  16.,  25.,  36.,  49.],
                                                  [   0.,   1.,   8.,  27.],
                                                  [   0.,   5.,  24.,  63.],
                                                  [   0.,  25.,  72., 147.],
                                                  [  64., 125., 216., 343.]])

        X = np.arange(0, 4).reshape(1, 4)
        X3 = map_feature(X, 3)
        print("X3={}".format(X3))
        np.testing.assert_array_almost_equal(X3, [[   0.,   1.,   2.,   3.],
                                                  [   0.,   1.,   4.,   9.],
                                                  [   0.,   1.,   8.,  27.]])

    def test_feature_normalize(self):
        X, y = load_flat_dataset(data_path="../../../data/ex1data2.txt")
        print(X[:, 0:10])
        X, mu, sigma= feature_normalize(X)
        print("X[:, 0:10]={}".format(X[:, 0:10]))
        print("mu={}".format(mu))
        print("sigma={}".format(sigma))

        np.testing.assert_array_almost_equal(X[:, 0:10], np.array([[1.300099e-001 , -2.236752e-001],
                                                                   [-5.041898e-001, -2.236752e-001],
                                                                   [5.024764e-001 , -2.236752e-001],
                                                                   [-7.357231e-001, -1.537767e+000],
                                                                   [1.257476e+000 ,  1.090417e+000],
                                                                   [-1.973173e-002,  1.090417e+000],
                                                                   [-5.872398e-001, -2.236752e-001],
                                                                   [-7.218814e-001, -2.236752e-001],
                                                                   [-7.810230e-001, -2.236752e-001],
                                                                   [-6.375731e-001, -2.236752e-001]]).T)



