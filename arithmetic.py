"""
Defines wrapper classes for decimal and floating point arthmatics. 
It gives the flexibility to the user code to work with different precisions at runtime.
"""

from abc import abstractmethod, abstractproperty
from math import ceil, log, floor, sqrt
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR


class Arithmetic:
    """
    Declares operations on a data type
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def ceil(self, value): pass
    
    @abstractmethod
    def floor(self, value): pass
    
    @abstractmethod
    def log(self, value, base): pass
    
    @abstractmethod
    def sqrt(self, value): pass
    
    @abstractmethod
    def cast(self, value): pass
    
    @abstractproperty
    def pinfty(self): pass
    
    @abstractproperty
    def ninfty(self): pass
    
class FloatArithmetic(Arithmetic):
    def ceil(self, value):
        return ceil(value)
    
    def floor(self, value):
        return floor(value)
    
    def log(self, value, base):
        return log(value, base)
    
    def sqrt(self, value):
        return sqrt(value)
    
    def cast(self, value):
        return float(value)
    
    @property
    def pinfty(self):
        return float('inf')
    @property
    def ninfty(self):
        return float('-inf')
    
class DecimalArithmetic(Arithmetic):
    def ceil(self, value):
        return value.to_integral_exact(rounding=ROUND_CEILING)
    
    def floor(self, value):
        return value.to_integral_exact(rounding=ROUND_FLOOR)
    
    def log(self, value, base):
        return value.ln() / base.ln()
    
    def sqrt(self, value):
        return value.sqrt()
    
    def cast(self, value):
        return Decimal(value)
    
    @property
    def pinfty(self):
        return Decimal('Infinity')
    
    @property
    def ninfty(self):
        return Decimal('-Infinity')