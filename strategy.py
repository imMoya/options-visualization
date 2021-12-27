import numpy as np
import matplotlib.pyplot as plt
from options import options

def inside_array(x_list):
    """ Return the min value a max value of an intersection of several arrays included in a list
    :param x_list: list with arrays inside
    :return min and max value of the intersection of the arrays in the x_list
    """
    x_min = 0
    x_max = 1e5
    for i in range(len(x_list)):
        x_min = np.min(x_list[i]) if np.min(x_list[i]) > x_min else x_min
        x_max = np.max(x_list[i]) if np.max(x_list[i]) < x_max else x_max
    return x_min, x_max

def closest(x, y, K):
    """Return the y(x closest to K)
    :param x: array (e.g. associated to x values in a plot)
    :param y: array (e.g. associated to y values in a plot)  
    :return y(x closest to K)
    """
    x = np.asarray(x)
    ind = (np.abs(x - K)).argmin()
    return y[ind]

class opt_inf():
    def __init__(self, K=0, pos='L', n=1):
        """Include information of options
        :param K: strike price at expiration date
        :param pos: type of position in an option ('L' if long, or 'S' if short)
        :param n: number of options """
        self.K = K
        self.pos = pos 
        self.n = n

class payoff_inf():
    def __init__(self, x, y):
        """Include two arrays (x, y) in an object
        :param x: array (e.g. associated to x values in a plot)
        :param y: array (e.g. associated to y values in a plot)  
        """
        self.x = x
        self.y = y

class strategy():
    def __init__(self, opt=[]):
        """Initialize the option class
        :param opt: option class (refer to opt_inf)
        """
        self.opt = opt

    def call(self):
        """Return the payoff of a call strategy with strike price K
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
        """Returns the payoff of different strategies.
        :param payoff: list of strategies defined (refer to main function)
        :return x: array containing prices surrounding the strike price of the strategy
        :return y: array containing the payoff for each price
        """
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
    """The main function returns the strategy defined to buy/sell different options.
    The user must define the payoff as a list of different strategies. 
    Each item in the list has to call the strategy class, defining the option:
        K (strike price)
        position ('L'/'S')
        n (number of options)
        call() or put()
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