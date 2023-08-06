import unittest
from qbz95.ml.utils import *
from qbz95.ml.planar_utils import *
from qbz95.ml.predictor import *
import qbz95.ml.linear_model as lm
from sklearn import metrics

# logger.setLevel(level=logging.DEBUG)


class TestPredictor(unittest.TestCase):
    pd.set_option('display.width', 100)

    def test_ClassificationPredictor_Binary(self):
        np.random.seed(3)
        predictor = ClassificationPredictor()

        X = np.abs(np.random.rand(1, 10))
        Y = np.array([[0, 1, 0, 1, 1, 1, 0, 1, 0, 1]])

        Y_predict = predictor.predict(X)
        print("X={}".format(X))
        print("Y={}".format(Y))
        print("Y_predict={}".format(Y_predict))

        np.testing.assert_array_equal(Y_predict, [[1, 1, 0, 1, 1, 1, 0, 0, 0, 0]])

        accuracy = predictor.accuracy(X, Y)
        print("accuracy={}".format(accuracy))
        np.testing.assert_allclose(accuracy, 0.7)
        metrics = predictor.evaluate(X, Y)
        print("metrics:\n{}".format(metrics))
        np.testing.assert_array_almost_equal(metrics.as_matrix(),
                                             [[0.7,  0, 0.6666667, 0.8, 0.75, 0.7272729,
                                               4,   2,   1,   3]])

    def test_ClassificationPredictor_Multi(self):
        np.random.seed(3)
        predictor = ClassificationPredictor()

        X = np.abs(np.random.rand(2, 10))
        Y = np.array([[0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 0, 0, 1, 0, 1, 0]])

        Y_predict = predictor.predict(X)
        print("X={}".format(X))
        print("Y={}".format(Y))
        print("Y_predict={}".format(Y_predict))

        np.testing.assert_array_equal(Y_predict, [[1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
                                                  [0, 0, 1, 0, 0, 0, 0, 1, 1, 0]])

        accuracy = predictor.accuracy(X, Y)
        print("accuracy={}".format(accuracy))
        np.testing.assert_allclose(accuracy, 0.7)

        metrics = predictor.evaluate(X, Y)
        print("metrics:\n{}".format(metrics))

        np.testing.assert_array_almost_equal(metrics.as_matrix(),
                                             [[0.7, 0, 0.833333,  0.714286,    0.500000, 0.769231,  5,  1,  2,  2],
                                              [0.7, 0, 0.500000,  0.666667,    0.833333, 0.571429,  2,  2,  1,  5]])

    def test_ProbabilityPredictor_Binary(self):
        np.random.seed(3)

        X = np.abs(np.random.rand(1, 10))
        Y = np.array([[0, 1, 0, 1, 1, 1, 0, 1, 0, 1]])
        predictor = ProbabilityPredictor.build(Y)
        np.testing.assert_array_almost_equal(predictor.prior_prob, [[0.6]])

        Y_predict = predictor.predict(X)
        print("X={}".format(X))
        print("Y={}".format(Y))
        print("Y_predict={}".format(Y_predict))

        np.testing.assert_array_equal(Y_predict, [[0, 1, 0, 0, 1, 1, 0, 0, 0, 0]])

        accuracy = predictor.accuracy(X, Y)
        print("accuracy={}".format(accuracy))
        np.testing.assert_allclose(accuracy, 0.7)
        metrics = predictor.evaluate(X, Y)
        print("metrics:\n{}".format(metrics))
        np.testing.assert_array_almost_equal(metrics.as_matrix(),
                                             np.array([[0.7,  0, 0.5, 1.0, 1.0, 0.666667,
                                                        3,   3,   0,   4]]))

    def test_ProbabilityPredictor_Multi(self):
        np.random.seed(3)
        X = np.abs(np.random.rand(3, 10))
        Y = np.array([[0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
                      [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
                      ])

        predictor = ProbabilityPredictor.build(Y)
        np.testing.assert_array_almost_equal(predictor.prior_prob, [[ 0.5], [ 0.3], [ 0.2]])

        Y_predict = predictor.predict(X)
        print("X={}".format(X))
        print("Y={}".format(Y))
        print("Y_predict={}".format(Y_predict))

        np.testing.assert_array_equal(Y_predict, [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                                  [1, 1, 1, 0, 1, 1, 1, 0, 1, 1]])

        accuracy = predictor.accuracy(X, Y)
        print("accuracy={}".format(accuracy))
        np.testing.assert_allclose(accuracy, 0.5333333)

        metrics = predictor.evaluate(X, Y)
        print("metrics:\n{}".format(metrics))

        np.testing.assert_array_almost_equal(metrics.as_matrix(),
                                             [[0.533333, 0, 0.2, 1.00, 1.000000, 0.333333,  1,  4,  0,  5],
                                              [0.533333, 0, 0.0, 0.00, 0.857143, 0.000000,  0,  3,  1,  6],
                                              [0.533333, 0, 1.0, 0.25, 0.250000, 0.400000,  2,  0,  6,  2]])


    def test_EvaluateCurve(self):
        train_X_orig, train_Y_orig, test_X_orig, test_Y_orig = load_petal_dataset()
        train_X, train_Y, test_X, test_Y = (train_X_orig, train_Y_orig, test_X_orig, test_Y_orig)
        train_X = map_feature(train_X, 3)
        test_X = map_feature(test_X, 3)
        model = lm.LogisticRegression(num_features=train_X.shape[0], activator=Sigmoid,
                                      regularizer=L2Regularizer(0), iterator=NumberIterator(100),
                                      optimizer=GradientOptimizer(0.5), initializer=WeightInitializer(),
                                      keep_cost_num_epoch=50)

        model.fit(train_X, train_Y, print_cost=False, print_num_epoch=50)
        metrics100 = EvaluateCurve.generate_data(train_X, train_Y, model=model)
        print("metrics100:\n{}".format(metrics100))

        auc = EvaluateCurve.auc(metrics=metrics100)
        sklearn_auc = metrics.auc(1 - metrics100["specificity"], metrics100['recall'])
        print("auc={}".format(auc))
        print("sklearn.auc={}".format(sklearn_auc))
        np.testing.assert_equal(auc, sklearn_auc)

        model.iterator = NumberIterator(200)
        model.fit(train_X, train_Y, print_cost=False, print_num_epoch=50)
        metrics200 = EvaluateCurve.generate_data(train_X, train_Y, model=model)
        print("metrics200:\n{}".format(metrics200))

        model.iterator = NumberIterator(400)
        model.fit(train_X, train_Y, print_cost=False, print_num_epoch=50)
        metrics400 = EvaluateCurve.generate_data(train_X, train_Y, model=model)
        print("metrics400:\n{}".format(metrics400))

        curves = {'NumberIterator(100)': metrics100,
                  'NumberIterator(200)': metrics200,
                  'NumberIterator(400)': metrics400}
        # EvaluateCurve.plot_roc(curves)
        # EvaluateCurve.plot_pr(curves)




