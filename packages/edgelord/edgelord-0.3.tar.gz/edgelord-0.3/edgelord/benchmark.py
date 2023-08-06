import numpy as np
import scipy.stats
from . import security as sc

class benchmark:
    """Benchmark stats for comparing one security to another"""
    security = None
    guage = None

    #
    #
    def __init__(self, security, benchmark_symbol):
        self.security = security
        self.guage = benchmark_symbol

    #
    #
    def alpha(self, days = None, price_type = 'close'):
        """Return the assets alpha in comparison to the guage"""

        rf = self.security.risk_free_rate
        security, guage = self.load_data(days, price_type)
        sg = (guage.iloc[-1] - guage.iloc[0]) / guage.iloc[0]
        mg = (security.iloc[-1] - security.iloc[0]) / security.iloc[0] 

        return ( (sg - rf) / (mg - rf) ) * self.beta(days, price_type)

    #
    #
    def beta(self, days = None, price_type = 'close'):
        """Return the assets beta in comparison to the guage"""
        data, guage = self.load_data(days, price_type)
        volatility = (data.std() / guage.std())
        result = self.correlation(days, price_type) * volatility

        return result

    #
    #
    def correlation(self, days = None, price_type = 'close'):
        """Return the correlation coeffecient between the two price arrays"""
        data, guage = self.load_data(days, price_type)

        if not len(data.index) == len(guage.index):
            
            if len(data.index) > len(guage.index):
                data = data.tail(len(guage.index)).reset_index()
            else:
                guage = guage.tail(len(data.index)).reset_index()
        
        return np.corrcoef(guage.values.tolist(), data.close.values.tolist())[0][1]

    #
    #
    def load_data(self, days = None, price_type = 'close'):
        """Load data for the time period"""
        
        if days is None:
            days = len(self.security.data.frame().index)
        
        return self.security.data.frame()[price_type].tail(days), self.guage.data.frame()[price_type].tail(days)

    #
    #
    def r_squared(self, days = None, price_type = 'close'):
        """Return the squared r value for the two securities"""

        sec = self.security.data.frame()[price_type].values.tolist()
        bm = self.guage.data.frame()[price_type].values.tolist()
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(sec, bm)
        
        return r_value**2