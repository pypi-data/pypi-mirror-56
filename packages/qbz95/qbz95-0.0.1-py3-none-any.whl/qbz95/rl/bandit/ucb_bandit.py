import numpy as np
from qbz95.rl.bandit.multi_armed_bandit import MultiArmedBandit, get_bandits
from qbz95.rl.bandit.epsilon_greedy_bandit import EpsilonGreedyBandit
from qbz95.rl.bandit.upper_limit_bandit import UpperLimitBandit
from qbz95.rl.bandit.delay_epsilon_bandit import DelayEpsilonBandit
import matplotlib.pyplot as plt


class UCBBandit(MultiArmedBandit):
    # Upper Confidence Bound

    def __init__(self, bandits):
        MultiArmedBandit.__init__(self, bandits)

    def pull(self):
        j = np.argmax([self.ucb(b) for b in self.bandits])
        return j, self.bandits[j].pull_update()

    def ucb(self, bandit):
        if bandit.n == 0:
            return float('inf')
        return bandit.mean_return + np.sqrt(2*np.log(len(self.returns)) / bandit.n)


if __name__ == "__main__":
    mab_bandit1 = UpperLimitBandit(get_bandits(10)).pulls(100000)
    mab_bandit2 = EpsilonGreedyBandit(get_bandits(), 0.1).pulls(100000)
    mab_bandit3 = UCBBandit(get_bandits()).pulls(100000)
    mab_bandit4 = DelayEpsilonBandit(get_bandits()).pulls(100000)
    mab_bandit1.plot_return(xscale="log", show=False, label='Upper Limit(ul=10)')
    mab_bandit2.plot_return(xscale="log", show=False, label='Epsilon Greedy(eps=0.1)')
    mab_bandit3.plot_return(xscale="log", show=False, label='UCB')
    mab_bandit4.plot_return(xscale="log", show=False, label='Delay Epsilon')
    plt.legend()
    plt.show()


