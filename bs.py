from scipy.stats import norm
import math

class Option:
    def __init__(self, call: bool, S: float, K: float, T: float,R: float,sigma:float):
        self.call=call
        self.S=S
        self.K=K
        self.t=T
        self.R=R
        self.sigma=sigma
        self.d1=(math.log(self.S/self.K)+R*self.t+(self.sigma**2*self.t/2))/(sigma*math.sqrt(self.t))
        self.d2= self.d1-self.sigma*math.sqrt(self.t)
        self.nd1=norm.cdf(self.d1)
        self.nd2=norm.cdf(self.d2)
        self.pdfd1=norm.pdf(self.d1)
        self.diff=1e-4
    def price(self):
        callprice = self.S*self.nd1-self.K*math.exp(-self.R*self.t)*self.nd2
        if self.call:
            return callprice
        else:
            pvK=self.K/(1+self.R)**self.t
            return callprice+pvK-self.S
#Greeks
    def delta(self):
        return (Option(self.call,self.S+self.diff,self.K,self.t,self.R,self.sigma).price()-self.price())/self.diff
    def gamma(self):
        return (Option(self.call,self.S+self.diff,self.K,self.t,self.R,self.sigma).delta()-self.delta())/self.diff
    def theta(self):
        return (self.price()-Option(self.call,self.S,self.K,self.t+self.diff,self.R,self.sigma).price())/self.diff
    def vega(self):
        return (Option(self.call,self.S,self.K,self.t,self.R,self.sigma+self.diff).price()-self.price())/self.diff/100
    def rho(self):
        return (Option(self.call,self.S,self.K,self.t,self.R+self.diff,self.sigma).price()-self.price())/self.diff/100
    def greeks(self):
        return {"delta":self.delta(),"gamma":self.gamma(),"theta":self.theta(),"vega":self.vega(),"rho":self.rho()}
    
class DividendOption(Option):
    def __init__(self,call: bool, S: float, K: float, T: float,R: float,q:float,sigma:float):
        super().__init__(call,S,K,T,R,sigma)
        self.q=q
        self.d1=(math.log(S/K)+(R-q)*self.t+(sigma**2*self.t/2))/(sigma*math.sqrt(self.t))
    
    def price(self):
        if self.call:
            return self.S*math.exp(-self.q*self.t)*self.nd1-self.K*math.exp(-self.R*self.t)*self.nd2
        else:
            return self.K*math.exp(-self.R*self.t)*norm.cdf(-self.d2)-self.S*math.exp(-self.q*self.t)*norm.cdf(-self.d1)
    def delta(self):
        return (DividendOption(self.call,self.S+self.diff,self.K,self.t,self.R,self.q,self.sigma).price()-self.price())/self.diff
    def gamma(self):
        return (DividendOption(self.call,self.S+self.diff,self.K,self.t,self.R,self.q,self.sigma).delta()-self.delta())/self.diff
    def theta(self):
        return (self.price()-DividendOption(self.call,self.S,self.K,self.t+self.diff,self.R,self.q,self.sigma).price())/self.diff
    def vega(self):
        return (DividendOption(self.call,self.S,self.K,self.t,self.R,self.q,self.sigma+self.diff).price()-self.price())/self.diff/100
    def rho(self):
        return (DividendOption(self.call,self.S,self.K,self.t,self.R+self.diff,self.q,self.sigma).price()-self.price())/self.diff/100

class FuturesOption(Option):
    def __init__(self, call: bool, S: float, K: float, T: float,R: float,sigma:float):
        super().__init__(call,S,K,T,R,sigma)
        self.d1=(math.log(self.S/self.K)+self.sigma**2*self.t/2)/(self.sigma*math.sqrt(self.t))
        self.d2= self.d1-self.sigma*math.sqrt(self.t)
        self.nd1=norm.cdf(self.d1)
        self.nd2=norm.cdf(self.d2)
        self.nnd1=norm.cdf(-self.d1)
        self.nnd2=norm.cdf(-self.d2)
    def price(self):
        if self.call:
            return math.exp(-self.R*self.t)*((self.S*self.nd1)-self.K*self.nd2)
        else:
            return math.exp(-self.R*self.t)*((self.K*self.nnd2)-self.S*self.nnd1)
    def delta(self):
        return (FuturesOption(self.call,self.S+self.diff,self.K,self.t,self.R,self.sigma).price()-self.price())/self.diff
    def gamma(self):
        return (FuturesOption(self.call,self.S+self.diff,self.K,self.t,self.R,self.sigma).delta()-self.delta())/self.diff
    def theta(self):
        return (self.price()-FuturesOption(self.call,self.S,self.K,self.t+self.diff,self.R,self.sigma).price())/self.diff
    def vega(self):
        return (FuturesOption(self.call,self.S,self.K,self.t,self.R,self.sigma+self.diff).price()-self.price())/self.diff/100
    def rho(self):
        return (FuturesOption(self.call,self.S,self.K,self.t,self.R+self.diff,self.sigma).price()-self.price())/self.diff/100

class ForexOption(Option):
    def __init__(self, call: bool, S: float, K: float, T: float,R: float,FR:float,sigma:float):
        super().__init__(call,S,K,T,R,sigma)
        self.FR=FR
        self.d1=(math.log(self.S/self.K)+(self.R-self.FR)*self.t+self.sigma**2*self.t/2)/(self.sigma*math.sqrt(self.t))
    def price(self):
        if self.call:
            return self.S*math.exp(-self.FR*self.t)*self.nd1-self.K*math.exp(-self.R*self.t)*self.nd2
        else:
            return self.K*math.exp(-self.R*self.t)*norm.cdf(-self.d2)-self.S*math.exp(-self.FR*self.t)*norm.cdf(-self.d1)
    def delta(self):
        return (ForexOption(self.call,self.S+self.diff,self.K,self.t,self.R,self.FR,self.sigma).price()-self.price())/self.diff
    def gamma(self):
        return (ForexOption(self.call,self.S+self.diff,self.K,self.t,self.R,self.FR,self.sigma).delta()-self.delta())/self.diff
    def theta(self):
        return (self.price()-ForexOption(self.call,self.S,self.K,self.t+self.diff,self.R,self.FR,self.sigma).price())/self.diff
    def vega(self):
        return (ForexOption(self.call,self.S,self.K,self.t,self.R,self.FR,self.sigma+self.diff).price()-self.price())/self.diff/100
    def rho(self):
        return (ForexOption(self.call,self.S,self.K,self.t,self.R+self.diff,self.FR,self.sigma).price()-self.price())/self.diff/100
