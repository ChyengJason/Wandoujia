#威尔逊置信区间
#以95%的置信区间
from math import sqrt

def confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.96 #1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    toplimit = ((phat + z*z/(2*n) + z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))
    bottomlimit =((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))

    return toplimit,bottomlimit
