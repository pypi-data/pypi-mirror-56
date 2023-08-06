import numpy as np


class Bandit:
    def __init__(self, mean, mean_return=0):
        self.mean = mean
        self.mean_return = mean_return
        self.n = 0

    def pull(self):
        ret = np.random.randn() + self.mean
        return ret

    def update(self, ret):
        self.n += 1
        self.mean_return = (1 - 1.0 / self.n) * self.mean_return + 1.0 / self.n * ret

    def pull_update(self):
        ret = self.pull()
        self.update(ret)
        return ret


class BonuliBandit(Bandit):
    def __init__(self, mean, mean_return=0):
        assert(mean <= 1)
        Bandit.__init__(self, mean, mean_return)
        self.win = 0
        self.lost = 0

    def pull(self):
        if np.random.randn() <= self.mean:
            return 1
        else:
            return 0

    def update(self, ret):
        self.n += 1
        self.mean_return = (1 - 1.0 / self.n) * self.mean_return + 1.0 / self.n * ret
        if ret > 0:
            self.win += 1
        else:
            self.lost += 1


