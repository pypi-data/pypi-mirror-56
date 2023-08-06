import numpy as np
import matplotlib.pyplot as plt
from qbz95.rl.bandit.bandit import Bandit, BonuliBandit


class MultiArmedBandit:
    def __init__(self, bandits):
        self.bandits = bandits
        self.returns = []
        self.n = 0
        self.mean_return = 0

    def pull(self):
        j = np.random.choice(len(self.bandits))
        return j, self.bandits[j].pull_update()

    def update(self, ret):
        self.n += 1
        self.returns.append(ret)
        self.mean_return = (1 - 1.0 / self.n) * self.mean_return + 1.0 / self.n * ret[1]

    def pulls(self, n=1):
        for i in range(n):
            self.update(self.pull())
        return self

    def get_cumulative_average(self):
        return np.cumsum([ret for _, ret in self.returns]) / (np.arange(self.n) + 1)

    def plot_return(self, xscale=None, show=True, label='', color="C0"):
        cumulative_average = self.get_cumulative_average()
        plt.plot(cumulative_average, linewidth=1, label=label, color=color)

        for i in range(len(self.bandits)):
            plt.plot(np.ones(self.n) * self.bandits[i].mean, '--', linewidth=1)
        if xscale is not None :
            plt.xscale(xscale)
        if show: plt.show()


def get_bandits(means=[1, 2, 3], mean_return=0):
    return [Bandit(mean=i, mean_return=mean_return) for i in means]


def get_bonuli_bandits(means=[0.2, 0.4, 0.6], mean_return=0):
    return [BonuliBandit(mean=i, mean_return=mean_return) for i in means]


if __name__ == "__main__":
    mab_bandit = MultiArmedBandit(get_bandits()).pulls(10000)
    mab_bandit.plot_return(xscale="log", color="C1")

