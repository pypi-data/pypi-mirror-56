import numpy as np
from qbz95.rl.bandit.multi_armed_bandit import MultiArmedBandit, get_bonuli_bandits
from qbz95.rl.bandit.epsilon_greedy_bandit import EpsilonGreedyBandit
from qbz95.rl.bandit.upper_limit_bandit import UpperLimitBandit
from qbz95.rl.bandit.delay_epsilon_bandit import DelayEpsilonBandit
from qbz95.rl.bandit.ucb_bandit import UCBBandit
import matplotlib.pyplot as plt
import pymc


class ThompsonSamplingBandit(MultiArmedBandit):

    def __init__(self, bandits):
        MultiArmedBandit.__init__(self, bandits)

    def pull(self):
        j = np.argmax([pymc.rbeta(1 + b.win, 1 + b.lost) for b in self.bandits])
        return j, self.bandits[j].pull_update()


if __name__ == "__main__":
    bandit_means = [0.5, 0.6, 0.7, 0.8, 0.9]
    times = 10000
    mab_bandits= [
        UpperLimitBandit(get_bonuli_bandits(bandit_means, mean_return=10)).pulls(times),
        EpsilonGreedyBandit(get_bonuli_bandits(bandit_means), 0.1).pulls(times),
        UCBBandit(get_bonuli_bandits(bandit_means)).pulls(times),
        DelayEpsilonBandit(get_bonuli_bandits(bandit_means)).pulls(times),
        ThompsonSamplingBandit(get_bonuli_bandits(bandit_means)).pulls(times)
    ]

    mab_bandits = sorted(mab_bandits, key=lambda mab_bandit: mab_bandit.mean_return )
    for i in range(len(mab_bandits)):
        mab_bandit = mab_bandits[i]
        label = type(mab_bandit).__name__ + ": {0:.5f}".format(mab_bandit.mean_return)
        mab_bandit.plot_return(xscale="log", show=False, label=label, color='C'+str(i % 8))

    plt.legend()
    plt.show()


