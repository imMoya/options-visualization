import numpy as np 

class options():
    def __init__(self, K, S=0):
        """
        :param S: stock price at expiration date
        :param K: strike price at expiration date
        :param S_array: array of stock prices near strike price
        """
        self.S = S
        self.K = K
        self.S_array = np.linspace(0.6*K, 1.4*K, 500)

    def payoff_call(self):
        """Return the payoff of a vanilla call option
        :param S: stock price at expiration date
        :param K: strike price at expiration date
        :return: payoff of the call option
        """
        return self.S-self.K if self.S>self.K else 0

    def payoff_put(self):
        """Return the payoff of a vanilla put option
        :param S: stock price at expiration date
        :param K: strike price at expiration date
        :return: payoff of the put option
        """
        return self.K-self.S if self.K>self.S else 0

    def payoff_call_bin(self):
        """Return the payoff of a binary call option
        :param S: stock price at expiration date
        :param K: strike price at expiration date
        :return: payoff of the call option
        """
        return 1 if self.S>self.K else 0

    def payoff_put_bin(self):
        """Return the payoff of a binary put option
        :param S: stock price at expiration date
        :param K: strike price at expiration date
        :return: payoff of the put option
        """
        return 1 if self.K>self.S else 0