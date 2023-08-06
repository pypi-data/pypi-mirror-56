#PBL Lidar Functions

import numpy as np
import math as m
from signal_analysis import mode
import sys
sys.path.append('/home/mach/Documents/AnE/Programming/Python/Signal_Processing')
import wavelets as wv
import pycuda_wavelets as py_wv
from scipy import signal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import signal_analysis as sa
import time

def idealbackscatterprof(bm,bu,zm,ezt,res,end): #supplies an ideal backscatter profile based on Steyn 1999
    z = np.arange(0,end+res,res) #height array at the desired resolution
    b = np.zeros(z.size)
    s = ezt/(1+np.pi**.5) #entrainment zone thickness variable
    A1 = (bm + bu)/2
    A2 = (bm - bu)/2
    for i in range(0,z.size):
        b[i] = A1 - A2*m.erf((z[i]-zm)/s) #ideal profile
    return z,b

def pbllayerh(wt,a,b):
    pklen = []
    peaks = []
    for i in range(a.size):
        pks,_ = signal.find_peaks(wt[i,:],height=(np.std(wt[i,:])*.5,None))
        peaks.append(pks)
        pklen.append(len(pks))
    pklen = np.array(pklen)
    err = 0
    try:
        md = mode(pklen[np.where(pklen!=0)[0]])
    except:
        while err == 0:
            try:
                pklen = pklen[0:-1]
                md = mode(pklen[np.where(pklen!=0)[0]])
                err = 1
            except:
                err = 0
                if len(pklen) == 0:
                    return np.nan,np.nan
    hi = np.where(pklen==md)[0][0]
    pblh = b[peaks[hi]]
    ezt = eztlayer(wt,a,b,peaks[hi])
    return pblh,ezt

def pbllayerh2(wt,a,b):
    pklen = []
    peaks = []
    for i in range(a.size):
        pks,_ = signal.find_peaks(wt[i,:])
        peaks.append(pks)
        pklen.append(len(pks))
    pklen = np.array(pklen)
    err = 0
    try:
        md = mode(pklen[np.where(pklen!=0)[0]])
    except:
        while err == 0:
            try:
                pklen = pklen[0:-1]
                md = mode(pklen[np.where(pklen!=0)[0]])
                err = 1
            except:
                err = 0
                if len(pklen) == 0:
                    return np.nan
    hi = np.where(pklen==md)[0][0]
    pblh2 = b[peaks[hi]]
    return pblh2

def eztlayer(wt,a,b,bi):
    ezt = np.zeros(bi.size)
    for i in range(bi.size):
        ai = np.where(wt[:,bi[i]]/a**.75==max(wt[:,bi[i]]/a**.75))[0][0]
        ezt[i] = a[ai]/2
    return ezt
    
def pblh(f,z):
    res = z[1]-z[0]
    a = np.arange(3*res,z[np.where(z<=2500)[0][-1]]+res,res)
    if np.isnan(f[0]):
        return np.nan,np.nan,np.nan,np.nan
    wt = wv.kwwt(f,z,a,z,5)
    pblh,ezt = pbllayerh(wt,a,z)
    pblh2 = pbllayerh2(wt,a,z)
    return pblh,pblh2,ezt

def cuda_pbl_layers(f,z):
    res = z[1]-z[0]
    a = np.arange(4*res,z[18]+res,res) #change to an end point of about 4 km if the height array is limited
    if np.isnan(f[0]): #checking for nan filled nrb files
        return []
    wt = py_wv.kwwt(f,z,a,z,5)
    wt = wt[0,:,:]
    wt = wv.clip_wavelet_kw(wt,a,z)
    pblh = pbl_layers(wt,z)
    return pblh

def pbl_layers(wt,b):
    wt = sa.moving_mean(wt[0,:],2)
    pks,_ = signal.find_peaks(wt)
    pblh = pks
    return pblh

#def cuda_pbl_layers(f,z):
#    res = z[1]-z[0]
#    a = np.arange(4*res,z[np.where(z<2000)[0][-1]]+res,res) #change to an end point of about 4 km if the height array is limited
#    if np.isnan(f[0]): #checking for nan filled nrb files
#        return []
#    wt = py_wv.kwwt(f,z,a,z,5)
#    wt = wt[0,:,:]
#    wt = wv.clip_wavelet_kw(wt,a,z)
#    pblh = pbl_layers(wt,z)
#    return pblh

#def pbl_layers(wt,b):
#    peaks = []
#    peaks_len = []    
#    for i in range(wt.shape[0]):
#        pks,_ = signal.find_peaks(wt[i,:])
#        peak,_ = signal.find_peaks(wt[i,:], height=np.mean(wt[i,pks]))
#        peaks_len.append(len(peak))
#        peaks.append(peak)
#    return peaks[np.where(np.array(peaks_len)==sa.mode(peaks_len))[0][0]]

#def pbl_layers(wt,b):
#    pklen = []
#    peaks = []
#    for i in range(wt.shape[0]):
#        pks,_ = signal.find_peaks(wt[i,:],height=(np.std(wt[i,:])*.5,None))
#        peaks.append(pks)
#        pklen.append(len(pks))
#    pklen = np.array(pklen)
#    err = 0
#    try:
#        md = mode(pklen[np.where(pklen!=0)[0]])
#    except:
#        while err == 0:
#            try:
#                pklen = pklen[0:-1]
#                md = mode(pklen[np.where(pklen!=0)[0]])
#                err = 1
#            except:
#                err = 0
#                if len(pklen) == 0:
#                    return np.nan,np.nan
#    hi = np.where(pklen==md)[0][0]
#    pblh = b[peaks[hi]]
#    return pblh

def run_pbl_layers(nrb,z,t):
    result = []
    for i in range(nrb[0,:].size):
        pblh = cuda_pbl_layers(nrb[:,i],z)
        result.append((i,[pblh]))
    return result
