import math
from .base_interest_rate import InterestRate

class Compound(InterestRate):
    

    def calulate_interest_rate(self):
        pass
    
    def calulate_present_value(self):
        pass
    
    def calulate_time(self):
        pass
    
    def calulate_future_value(self):
        self.future_value = self.present_value * math.pow(1.0+self.interest_rate, self.time)
        return self.future_value
        
    
    