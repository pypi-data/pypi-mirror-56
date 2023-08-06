import numpy as np

class Shake:
    def __init__(self, **kwargs):
        pass

    def update_rule(**kwargs):
        pass

    def apply(self, current, neighbors):
        odd = current[1::2]
        even = current[::2]

        state0 = (current==0)
        stateL = (current==L)
        stateR = (current==R)
        state1 = (current==1)

