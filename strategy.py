import numpy as np
import matplotlib.pyplot as plt
from options import options

def inside_array(x_list):
    x_min = 0
    x_max = 1e5
    for i in range(len(x_list)):
        x_min = np.min(x_list[i]) if np.min(x_list[i]) > x_min else x_min
        x_max = np.max(x_list[i]) if np.max(x_list[i]) < x_max else x_max
    return x_min, x_max

def closest(x, y, K):
     x = np.asarray(x)
     ind = (np.abs(x - K)).argmin()
     return y[ind]

class opt_inf():
    def __init__(self, K=0, pos='L', n=1):
        self.K = K
        self.pos = pos 
        self.n = n

class payoff_inf():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class strategy():
    def __init__(self, opt=[]):
        self.opt = opt

    def call(self):
        """Return the payoff of a call strategy with strike price K1
        """
        K = self.opt.K
        pos = 1 if self.opt.pos == 'L' else -1
        n = self.opt.n

        payoff = [pos * n * options(K=K, S=S_).payoff_call() for S_ in options(K=K).S_array] 

        return payoff_inf(x=options(K=K).S_array, y=payoff)
    
    def put(self):
        """Return the payoff of a put strategy with strike price K1
        """
        K = self.opt.K
        pos = 1 if self.opt.pos == 'L' else -1
        n = self.opt.n

        payoff = [pos * n * options(K=K, S=S_).payoff_put() for S_ in options(K=K).S_array] 
        
        return payoff_inf(x=options(K=K).S_array, y=payoff)

    @staticmethod
    def combine(payoff):
        x_list = []
        [x_list.append(p.x) for p in payoff]
        x_min, x_max = inside_array(x_list)
        x = np.linspace(x_min, x_max, 500)
        y = np.linspace(0, 0, len(x))
        for i in range(len(x)): 
            for p in payoff:
                y[i] += closest(p.x, p.y, x[i])
        
        return x, y

def main():
    """The main function returns the strategy defined.
    """
    payoff = [strategy(opt=opt_inf(K=1, pos='L', n=2)).call(),
              strategy(opt=opt_inf(K=1, pos='L', n=2)).put()]
    x, y = strategy().combine(payoff)
    plt.plot(x, y)
    plt.xlabel('Asset price')
    plt.ylabel('Strategy payoff')
    plt.show()

if __name__ == "__main__":
    main() 