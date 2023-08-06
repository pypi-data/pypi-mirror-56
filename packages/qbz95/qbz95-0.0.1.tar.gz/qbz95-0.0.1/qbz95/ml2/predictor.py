import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from sklearn.metrics import roc_auc_score, roc_curve, auc, precision_recall_curve, average_precision_score


class ClassificationPredictor(object):
    def __init__(self, model):
        self.model = model

    def predict(self, X):
        pass

    def accuracy(self, X, y):
        pass

    def accuracy_(self, y_pred, y):
        return np.mean(y_pred == y)

    def evaluate(self, X, y):
        pass

    def evaluates(self, X_train, y_train, X_val=None, y_val=None, X_test=None, y_test=None):
        metrics = []
        if X_train is not None:
            metrics_ = self.evaluate(X_train, y_train)
            metrics_ = pd.DataFrame([metrics_.values()], index=["train"], columns=metrics_.keys())
            metrics.append(metrics_)
        if X_val is not None:
            metrics_ = self.evaluate(X_val, y_val)
            metrics_ = pd.DataFrame([metrics_.values()], index=["val"], columns=metrics_.keys())
            metrics.append(metrics_)
        if X_test is not None:
            metrics_ = self.evaluate(X_test, y_test)
            metrics_ = pd.DataFrame([metrics_.values()], index=["test"], columns=metrics_.keys())
            metrics.append(metrics_)
        return pd.concat(metrics)


class MultiClassificationPredictor(ClassificationPredictor):

    def __init__(self, model):
        ClassificationPredictor.__init__(self, model)

    def predict(self, X):
        return np.argmax(self.model.predict(X), axis=-1)

    def accuracy(self, X, y):
        y_pred = self.predict(X)
        y = np.argmax(y, axis=-1)
        return self.accuracy_(y_pred, y)

    def evaluate(self, X, y):
        y_pred = self.predict(X)
        y = np.argmax(y, axis=-1)
        accuracy = self.accuracy_(y_pred, y)
        return {"accuracy":accuracy}


class BinaryClassificationPredictor(ClassificationPredictor):

    def __init__(self, model, cutoff=0.5):
        ClassificationPredictor.__init__(self, model)
        self.cutoff = cutoff

    def predict(self, X):
        return np.int32(self.model.predict(X) > self.cutoff).flatten()

    def accuracy(self, X, y):
        y_pred = self.predict(X)
        return self.accuracy_(y_pred, y)

    def evaluate(self, X, y):
        metrics = OrderedDict()
        y_pred = self.predict(X)
        accuracy = self.accuracy_(y_pred, y)
        metrics["accuracy"] = accuracy

        tp = np.sum((y_pred == 1) * (y == 1)) * 1.0
        fn = np.sum((y_pred == 0) * (y == 1)) * 1.0
        fp = np.sum((y_pred == 1) * (y == 0)) * 1.0
        tn = np.sum((y_pred == 0) * (y == 0)) * 1.0

        recall = tp / (tp + fn) if tp > 0 else 0
        precision = tp / (tp + fp) if tp > 0 else 0
        specificity = tn / (tn + fp) if tn > 0 else 0
        f1 = 2 * recall * precision / (recall + precision) if recall + precision > 0 else 0

        metrics["recall"] = recall
        metrics["precision"] = precision
        metrics["specificity"] = specificity
        metrics["f1"] = f1
        metrics["tp"] = tp
        metrics["fn"] = fn
        metrics["fp"] = fp
        metrics["tn"] = tn

        return metrics


class EvaluateCurve(object):
    def __init__(self, y_true, y_scores):
        y_scores = y_scores.flatten()
        self.fpr, self.tpr, self.roc_thresholds = roc_curve(y_true, y_scores)
        self.auc = auc(self.fpr, self.tpr)

        self.precision, self.recall, self.pr_thresholds = precision_recall_curve(y_true, y_scores)
        self.ap = average_precision_score(y_true, y_scores)

    def plot_roc(self):
        plt.title('ROC Curve [AUC={:.4f}]'.format(self.auc))
        plt.xlim((-0.05, 1.05))
        plt.ylim((-0.05, 1.05))
        plt.ylabel('Sensitivity(TPR)')
        plt.xlabel('1-Specificity(FPR)')
        plt.xticks(np.linspace(0, 1, 11))
        plt.yticks(np.linspace(0, 1, 11))

        plt.plot(self.fpr, self.tpr,  lw=1)

        plt.plot([0,1],[0,1], '--', color='k')
        plt.show()

    def plot_pr(self):
        plt.title('Precision-Recall [AP={:.4f}]'.format(self.ap))
        plt.xlim((0, 1))
        plt.ylim((0, 1.05))
        plt.ylabel('Precision')
        plt.xlabel('Recall')
        plt.xticks(np.linspace(0, 1, 11))
        plt.yticks(np.linspace(0, 1, 11))


        # plt.plot(self.recall, self.precision, lw=1 )
        plt.step(self.recall, self.precision, color='b', alpha=0.2,
                 where='post')
        plt.fill_between(self.recall, self.precision, step='post', alpha=0.2,
                         color='b')
        plt.show()