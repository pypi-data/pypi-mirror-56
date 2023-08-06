# PCA with SVD

import numpy as np

def fct_SVD(X, nbPC):
    s0, s1 = X.shape
    T = np.zeros(shape=(s0, nbPC))
    P = np.zeros(shape=(s1, nbPC))
    SSX = np.zeros(shape=(nbPC, 1))
    X0 = X # Save a copy

    for i in range(0,nbPC):
        # SVD of X*X' gives T
        [V,D,VT] = np.linalg.svd(X @ X.T)    
        t = V[:,0] * np.linalg.norm(X,2)
        t = np.reshape(t,(s0,1))
        T[:,i] = np.squeeze(t) 

        # SVD of X'*X gives P
        [V,D,VT] = np.linalg.svd(X.T @ X)    
        p = V[:,0] 
        p = np.reshape(p,(s1,1))
        P[:,i] = np.squeeze(p) # Remove single-dimensional entries from the shape of an array.
        
        # Deflation: Carrying out independant SVD calculations causes some problems.
        # The signs do not necessarily line up (rotational ambiguity).
        direction = np.sum(np.sum(X*(t@p.T)))
        if direction <= 0:
            p = -1*p
        
        X = X - t@p.T
    
        # Sum of squares -----------
        Xhat = t@p.T
        ssX0 = np.sum(np.sum(X0 * X0)) # Each element squared
        ssX = np.sum(np.sum(Xhat * Xhat))
        ssX = ssX / ssX0
        SSX[i] = ssX
        # --------------------------
    
    # % Varience explained by the model
    #Varex = np.sum(SSX)
    
   
    
    return T, P, SSX