import numpy as np
from qbz95.rl.bandit.multi_armed_bandit import MultiArmedBandit, get_bandits
from qbz95.rl.bandit.epsilon_greedy_bandit import EpsilonGreedyBandit
from qbz95.rl.bandit.bandit import Bandit
import matplotlib.pyplot as plt


class UpperLimitBandit(MultiArmedBandit):
    def __init__(self, bandits):
        MultiArmedBandit.__init__(self, bandits)

    def pull(self):
        j = np.argmax([b.mean_return for b in self.bandits])
        return j, self.bandits[j].pull_update()


if __name__ == "__main__":
    mab_bandit1 = UpperLimitBandit(get_bandits(10)).pulls(100000)
    mab_bandit2 = EpsilonGreedyBandit(get_bandits(), 0.1).pulls(100000)
    mab_bandit1.plot_return(xscale="log", show=False, label='Upper Limit')
    mab_bandit2.plot_return(xscale="log", show=False, label='Epsilon Greedy(eps=0.1)')
    plt.legend()
    plt.show()


