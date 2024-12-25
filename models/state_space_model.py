import numpy as np
from scipy import signal

class StateSpaceModel:
    def __init__(self,
                 A:np.ndarray,
                 B:np.ndarray,
                 C:np.ndarray,
                 D:np.ndarray
                 ):
        self.system = signal.StateSpace(A,B,C,D)

    def gen(self):
        return self.system
