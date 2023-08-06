import matplotlib.pyplot as plt


class Model(object):
    def __init__(self):
        self.costs = []

    def activate(self, X):
        return X

    def get_cost(self, X, Y):
        return 0

    def plot_costs(self, title=None, xlabel="epochs", ylabel="cost", costs=None):
        if costs is None:
            costs = self.costs
        plt.plot(costs)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.show()


