#Wavelet Analysis and Transform minipackage

#Written by Doug Keller

import numpy as np

def kw(x,a,b,n): #complex frequency function windowed by a super Gaussian function
    return (np.exp(((2*np.pi*(x-b)/a)+np.pi/2)*(-1)**.5)*(.01)**((2*(x-b)/a)**(2*n))).real #modified Morlet wavelet but with a super Gaussian (only taking the real part or the part that forms a sine wave in the real domain)

def dgw(x,a,b,n): #Super Gaussian function first derivative wavelet
    return ((x-b)/a)**(2*n-1)*np.exp(.5-.5*((x-b)/a)**(2*n))

def sgw(x,a,b,n,y_a): #Super Gaussian function wavelet
    return y_a ** ((x - b) *2/a) ** (2*n)
    
def kwwt(f,x,a,b,n): #wavelet transform with the sine/super Gaussian wavelet
    phi = np.zeros((x.size,b.size,a.size))
    for ai in range(0,a.size):
        for bi in range(0,b.size):
            for xi in range(0,x.size):
                phi[xi,bi,ai] = kw(x[xi],a[ai],b[bi],n)
    fphi = np.tensordot(f,phi,1)
    wt = np.transpose(np.zeros(fphi.shape))
    for ai in range(0,a.size):
        wt[ai,:] = fphi[:,ai]/a[ai]**.5
    return wt
  
#def kwwt1(f,x,a,b,n): #wavelet transform with the sine/super Gaussian wavelet
#    wt = np.zeros((a.size,b.size))
#    for ai in range(0,a.size):
#        for bi in range(0,b.size):
#            for xi in range(0,x.size):
#                wt[ai,bi] += f[xi] * kw(x[xi],a[ai],b[bi],n) / a[ai]**.5
#    return wt

def sgwwt(f,x,a,b,n,y_a): #wavelet transform with the Gaussian function wavelet
    phi = np.zeros((x.size,b.size,a.size))
    for ai in range(0,a.size):
        for bi in range(0,b.size):
            for xi in range(0,x.size):
                phi[xi,bi,ai] = sgw(x[xi],a[ai],b[bi],n,y_a)
    fphi = np.tensordot(f,phi,1)
    wt = np.transpose(np.zeros(fphi.shape))
    for ai in range(0,a.size):
        wt[ai,:] = fphi[:,ai]/a[ai]**.5
    return wt

def clip_wavelet_kw(wt,a,b):
    for i in range(a.size):
        for j in range(b.size):
            if b[j] < b[0] + a[i]/2 or b[j] > b[-1] - a[i]/2:
                wt[i,j] = np.nan
    return wt