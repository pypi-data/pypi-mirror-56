#PBL Lidar Functions

import numpy as np
import math as m
import os
os.chdir('..')
os.chdir('..')

def idealbackscatterprof(bm,bu,zm,ezt,res,end): #supplies an ideal backscatter profile based on Steyn 1999
    z = np.arange(0,end+res,res) #height array at the desired resolution
    b = np.zeros(z.size)
    s = ezt/(1+np.pi**.5) #entrainment zone thickness variable
    A1 = (bm + bu)/2
    A2 = (bm - bu)/2
    for i in range(0,z.size):
        b[i] = A1 - A2*m.erf((z[i]-zm)/s) #ideal profile
    return z,b