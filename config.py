"""
Defines the main settings including the type of precision used in the program.
"""

from arithmetic import FloatArithmetic


class Config:
    def __init__(self, arithmetic = FloatArithmetic()):
        self.arithmatic = arithmetic
        
config = Config()