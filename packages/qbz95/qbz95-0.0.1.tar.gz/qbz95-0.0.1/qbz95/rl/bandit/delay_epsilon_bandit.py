import numpy as np
from qbz95.rl.bandit.multi_armed_bandit import MultiArmedBandit, get_bandits
from qbz95.rl.bandit.epsilon_greedy_bandit import EpsilonGreedyBandit
import matplotlib.pyplot as plt


class DelayEpsilonBandit(MultiArmedBandit):
    def __init__(self, bandits):
        MultiArmedBandit.__init__(self, bandits)

    def pull(self):
        p = np.random.random()
        if p < 1/(len(self.returns) + 1):
            j = np.random.choice(len(self.bandits))
        else:
            j = np.argmax([b.mean_return for b in self.bandits])
        return j, self.bandits[j].pull_update()


if __name__ == "__main__":
    mab_bandit1 = DelayEpsilonBandit(get_bandits()).pulls(100000)
    mab_bandit2 = EpsilonGreedyBandit(get_bandits(), 0.1).pulls(100000)
    mab_bandit1.plot_return(xscale="log", show=False, label='Delay Epsilon')
    mab_bandit2.plot_return(xscale="log", show=False, label='Epsilon Greedy(eps=0.1)')
    plt.legend()
    plt.show()


