import numpy as np

def MaxMinNormalization(x,Max,Min):
    x = (x - Min) / (Max - Min)
    return x

def Z_ScoreNormalization(x,mu,sigma):
    #mu（即均值）用np.average()，sigma（即标准差）用np.std()
    x = (x - mu) / sigma
    return x

def sigmoid(X,useStatus):
    if useStatus:
        return 1.0 / (1 + np.exp(-float(X)))
    else:
        return float(X)

for i in range(-10,10,1):
    print(i,end=" ")
    print(sigmoid(i,True))