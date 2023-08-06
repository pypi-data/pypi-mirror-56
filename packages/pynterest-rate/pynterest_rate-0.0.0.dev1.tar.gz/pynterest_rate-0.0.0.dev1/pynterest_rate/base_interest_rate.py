from abc import ABC, abstractmethod

class InterestRate(ABC):
    
    def __init__(self, i=None, pv=None, t=None, fv=None):
        """ Generic Interest rate class for calculating and 
        visualizing a interest rate
        
        Paramters
        ---------
        i (float) Interest rate, ex 0.5
        pv (float) representing the present value
        t (float) time which the interests are colleted
        fv (float) future value
        """
        self.interest_rate = i
        self.present_value = pv
        self.time = t
        self.future_value = pv
    
    @abstractmethod
    def calulate_interest_rate(self):
        pass
    
    @abstractmethod
    def calulate_present_value(self):
        pass
    
    @abstractmethod
    def calulate_time(self):
        pass
    
    @abstractmethod
    def calulate_future_value(self):
        pass
        
