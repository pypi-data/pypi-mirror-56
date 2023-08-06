# Flip score as needed - rotational ambiguity

import numpy as np


def fct_flip(X,Y):
    s0, s1 = X.shape
    for i in range(0,s1):
        x = X[:,i]
        y = Y[:,i]
        
        if x.T @ y < 0: y = -1*y
        
        Y[:,i] = np.squeeze(y)
        
    return Y