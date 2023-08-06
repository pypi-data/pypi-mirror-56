import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qbz95.ml.utils import logger
from qbz95.ml.planar_utils import plot_decision_boundary
from qbz95.ml.model import Model
from sklearn import metrics


class Predictor(object):
    def __init__(self, model=Model()):
        self.model = model

    def predict(self, X):
        logger.debug("X.shape={}".format(X.shape))
        A = self.model.activate(X)
        logger.debug("A.shape={}".format(A.shape))
        return self.predict_(A)

    def predict_(self, A):
        return A

    def plot_regression_curve(self, X, y, title="regression", X_model=None):
        '''
        only work for X which only have 2 features.
        :param X:  (2, num_sample)
        :param y:  (1, num_sample)
        :param title:
        :return:
        '''
        if len(X.shape) == 2 and X.shape[0] == 1 and len(y.shape) == 2 and y.shape[0] == 1:
            plt.title(title)
            axes = plt.gca()
            min = X.min(axis=1)
            max = X.max(axis=1)
            range = max - min
            min = min - 0.1 * range
            max = max + 0.1 * range
            axes.set_xlim((min[0], max[0]))
            min = y.min(axis=1)
            max = y.max(axis=1)
            range = max - min
            min = min - 0.1 * range
            max = max + 0.1 * range
            axes.set_ylim((min[0], max[0]))
            y_predict =  self.predict(X) if X_model is None else self.predict(X_model)

            plt.scatter(X.T, y.T, c='C0', s=10, cmap=plt.cm.Spectral)

            order = np.lexsort((y_predict, X))
            X, y_predict = X[0, order], y_predict[0, order]
            plt.plot(X.T, y_predict.T, 'C1-')
            plt.show()
        else:
            print("plot_regression_curve only works for X which only have 1 features.")


class ClassificationPredictor(Predictor):

    def __init__(self, model=Model()):
        Predictor.__init__(self, model)

    def predict_(self, A):
        if A.shape[0] == 1:
            return np.int32(A > 0.5)
        else:
            a_max = np.max(A, axis=0, keepdims=True)
            return  np.int32(A == a_max)

    def accuracy(self, X, Y):
        Y_predict = self.predict(X)
        return self.accuracy_(Y_predict, Y)

    def accuracy_(self, Y_predict, Y):
        return np.mean(Y_predict == Y)

    def evaluate(self, X, Y, index = None):
        Y_predict = self.predict(X)
        accuracy = self.accuracy_(Y_predict, Y)
        cost = self.model.get_cost(X, Y)
        k = Y.shape[0]
        metrics = []
        for i in range(k):
            tp = np.sum((Y_predict[i]==1) * (Y[i]==1))
            fn = np.sum((Y_predict[i]==0) * (Y[i]==1))
            fp = np.sum((Y_predict[i]==1) * (Y[i]==0))
            tn = np.sum((Y_predict[i]==0) * (Y[i]==0))

            recall = tp/(tp+fn) if tp>0 else 0
            precision = tp/(tp+fp) if tp>0 else 0
            specificity = tn/(tn+fp) if tn>0 else 0
            f1 = 2*recall*precision/(recall+precision) if recall+precision>0 else 0

            metrics.append([accuracy, cost, recall, precision, specificity, f1, tp, fn, fp, tn])

        if index is None:
            index = range(k)
        metrics = pd.DataFrame(metrics, index=index,
                               columns=['accuracy', 'cost', 'recall', 'precision', 'specificity', 'f1',  'tp', 'fn', 'fp', 'tn'])
        return metrics

    def print_metrics(self, train_X, train_Y, dev_X=None, dev_Y=None, test_X=None, test_Y=None):
        metrics = []
        if train_X is not None:
            metrics_ = self.evaluate(train_X, train_Y)
            metrics_.index=["train"]
            metrics.append(metrics_)
        if dev_X is not None:
            metrics_ = self.evaluate(dev_X, dev_Y)
            metrics_.index = ["dev"]
            metrics.append(metrics_)
        if test_X is not None:
            metrics_ = self.evaluate(test_X, test_Y)
            metrics_.index = ["test"]
            metrics.append(metrics_)
        print(pd.concat(metrics))

    def print_accuracy(self, X, Y, title="train"):
        print("{} accuracy: {}".format(title, self.accuracy(X, Y)))

    def print_accuracy_train_test(self, train_X, train_Y, dev_X=None, dev_Y=None, test_X=None, test_Y=None):
        if train_X is not None:
            self.print_accuracy(train_X, train_Y, "train")
        if dev_X is not None:
            self.print_accuracy(dev_X, dev_Y, "dev")
        if test_X is not None:
            self.print_accuracy(test_X, test_Y, "test")

    def plot_decision_boundary(self, X, y, title="decision boundary"):
        '''
        only work for X which only have 2 features.
        :param X:  (2, num_sample)
        :param y:  (1, num_sample)
        :param title:
        :return:
        '''
        if len(X.shape)==2 and X.shape[0]==2 and len(y.shape)==2 and y.shape[0]==1:
            plt.title(title)
            axes = plt.gca()
            min = X.min(axis=1)
            max = X.max(axis=1)
            range = max - min
            min = min - 0.1 * range
            max = max + 0.1 * range
            axes.set_xlim((min[0], max[0]))
            axes.set_ylim((min[1], max[1]))
            plot_decision_boundary(lambda x: self.predict(x.T), X, y)
        else:
            print("plot_decision_boundary only works for X which only have 2 features.")


class ProbabilityPredictor(ClassificationPredictor):

    @classmethod
    def build(cls, train_Y, model=Model()):
        k = train_Y.shape[0]
        m = train_Y.shape[1]
        positive_prob = np.array([np.sum(train_Y[i] == 1)/m for i in range(k)]).reshape((k, 1))
        if k==1:
            prior_prob = positive_prob
        else:
            prior_prob = positive_prob/np.sum(positive_prob)
        return ProbabilityPredictor(prior_prob, model)

    def __init__(self, prior_prob=0.5, model=Model()):
        ClassificationPredictor.__init__(self, model)
        logger.debug("prior_prob={}".format(prior_prob))
        self.prior_prob = prior_prob

    def predict_(self, A):
        if A.shape[0] == 1:
            return np.int32(A > self.prior_prob)
        else:
            A_adjust = A/self.prior_prob
            logger.debug("A_adjust[0:20, 0:20]={}".format(A_adjust[0:20, 0:20]))
            A_adjust_max = np.max(A_adjust, axis=0, keepdims=True)
            return  np.int32(A_adjust == A_adjust_max)


class EvaluateCurve(object):
    # def __init__(self, model=Model()):
    #     Predictor.__init__(self, model)

    @classmethod
    def generate_data(cls, X, Y, model=Model(), cutoffs=np.linspace(1, 0, num=21)):
        assert(Y.shape[0]==1)
        A = model.activate(X)

        cutoff_metrics = []
        for cutoff in cutoffs:
            predictor = ProbabilityPredictor(cutoff, model)
            metrics = predictor.evaluate(X, Y)
            metrics.insert(0, "cut_off", cutoff)
            cutoff_metrics.append(metrics)

        cutoff_metrics = pd.concat(cutoff_metrics)
        cutoff_metrics.index = np.arange(0, len(cutoffs))
        return cutoff_metrics

    @classmethod
    def auc(cls, fpr=None, tpr=None, metrics=None):
        if metrics is None:
            return np.trapz(tpr, fpr)
        else:
            return np.trapz(metrics['recall'], 1 - metrics["specificity"])

    @classmethod
    def plot_roc(cls, cutoffs):
        plt.title('ROC Curve')
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        plt.ylabel('Sensitivity(TPR)')
        plt.xlabel('1-Specificity(FPR)')
        plt.xticks(np.linspace(0, 1, 11))
        plt.yticks(np.linspace(0, 1, 11))

        m = len(cutoffs)
        i = 0
        for label, metrics in cutoffs.items():
            plt.plot(1-metrics["specificity"], metrics["recall"], 'C'+str(i % 10)+".-")
            i = i + 1
        plt.legend(cutoffs.keys(), loc='lower right')
        plt.plot([0,1],[0,1], '--', color='k')
        plt.show()

    @classmethod
    def plot_pr(cls, cutoffs):
        plt.title('Recall Precision')
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        plt.ylabel('Recall')
        plt.xlabel('Precision')
        plt.xticks(np.linspace(0, 1, 11))
        plt.yticks(np.linspace(0, 1, 11))

        m = len(cutoffs)
        i = 0
        for label, metrics in cutoffs.items():
            plt.plot(metrics["precision"], metrics["recall"], 'C'+str(i % 10)+".-")
            i = i + 1
        plt.legend(cutoffs.keys(), loc='lower left')

        plt.show()
