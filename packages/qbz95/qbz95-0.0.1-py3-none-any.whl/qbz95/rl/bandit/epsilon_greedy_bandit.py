import numpy as np
from qbz95.rl.bandit.multi_armed_bandit import MultiArmedBandit, get_bandits
from qbz95.rl.bandit.bandit import Bandit
import matplotlib.pyplot as plt


class EpsilonGreedyBandit(MultiArmedBandit):
    def __init__(self, bandits, epsilon):
        MultiArmedBandit.__init__(self, bandits)
        self.epsilon = epsilon

    def pull(self):
        p = np.random.random()
        if p < self.epsilon:
            j = np.random.choice(len(self.bandits))
        else:
            j = np.argmax([b.mean_return for b in self.bandits])
        return j, self.bandits[j].pull_update()



if __name__ == "__main__":
    mab_bandit1 = EpsilonGreedyBandit(get_bandits(), 0.01).pulls(100000)
    mab_bandit2 = EpsilonGreedyBandit(get_bandits(), 0.05).pulls(100000)
    mab_bandit3 = EpsilonGreedyBandit(get_bandits(), 0.1).pulls(100000)
    mab_bandit1.plot_return(xscale="log", show=False, label='0.01')
    mab_bandit2.plot_return(xscale="log", show=False, label='0.05')
    mab_bandit3.plot_return(xscale="log", show=False, label='0.1')
    plt.legend()
    plt.show()


