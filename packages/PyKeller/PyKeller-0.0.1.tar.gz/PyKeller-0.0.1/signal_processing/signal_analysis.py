#Signal Analysis general functions

import numpy as np
import collections
import math as m
from scipy.interpolate import interp1d

def moving_mean(f,N):
    
    mm = np.zeros(f.size)
    
    for i in range(f.size):
        if i < N:
            m = []
            for j in range(i+N+1):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.mean(m)
        elif i+N > f.size-1:
            m = []
            for j in range(i-N,f.size):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.mean(m)
        else:
            mm[i] = np.mean(f[i-N:i+N+1][np.where(np.isfinite(f[i-N:i+N+1]))[0]])
        
    return mm

def moving_median(f,N):
    
    mm = np.zeros(f.size)
    
    for i in range(f.size):
        if i < N:
            m = []
            for j in range(i+N+1):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.median(m)
        elif i+N > f.size-1:
            m = []
            for j in range(i-N,f.size):
                if np.isfinite(f[j]):
                    m.append(f[j])
            m = np.array(m)
            mm[i] = np.median(m)
        else:
            mm[i] = np.median(f[i-N:i+N+1][np.where(np.isfinite(f[i-N:i+N+1]))[0]])
        
    return mm

def brock_improved_despike(f,N):
    #Improved version of Brock's "A Nonlinear Filter to Remove Impulse Noise from Meteorological Data," 1986, JTECH
    
    def run_despike(f,f_med):
        
        dif = f - f_med
        dif_max = np.nanmax(dif) - np.nanmin(dif)
        dif_min = np.sort(np.abs(np.diff(dif)))
        dif_min = dif_min[np.where(dif_min>0)[0]]
        dif_min = 2*np.nanmin(dif_min)
        
        bin_max = int(dif_max//dif_min)
        
        spikes = 0
        spike_loc = []
        bin_count = 3
        while bin_count < bin_max:
            hist,bins = np.histogram(dif,bins=bin_count)
            
            dif_threshold = [bins[0],bins[-1]]
            zeros = np.where(hist==0)[0]
            if len(zeros) > 0:
                bins_mean = np.where(hist==max(hist))[0][0]
                
                zero_mid = zeros - bins_mean
                zero_gn = zero_mid[np.where(zero_mid<0)[0]]
                zero_lp = zero_mid[np.where(zero_mid>=0)[0]]
                
                if len(zero_gn) > 0:
                    zero_gn = max(zero_gn) + bins_mean
                    dif_threshold[0] = bins[zero_gn]
                
                if len(zero_lp) > 0:
                    zero_lp = min(zero_lp) + bins_mean
                    dif_threshold[1] = bins[zero_lp+1]
                
                for i in range(len(f)):
                    if dif[i] > dif_threshold[1]:
                        f[i] = f_med[i]
                        spike_loc.append(i)
                        spikes += 1
                    if dif[i] < dif_threshold[0]:
                        f[i] = f_med[i]
                        spike_loc.append(i)
                        spikes += 1
                
                bin_count = bin_max
            
            bin_count += 2
            
        return f, spikes, spike_loc
    
    f = np.array(f)
    f_med = moving_median(f,N)
    
    f,spikes,spike_loc = run_despike(f,f_med)
    spike = [spikes]
    slc = spike_loc
    while spikes > 0:
        f,spikes,spike_loc = run_despike(f,f_med)
        spike.append(spikes)
        slc += spike_loc
        
    return f,spike,slc

def super_sample(f,x):
    
    x_ss = []
    dx = np.diff(x)
    for i in range(x.size-1):
        x_ss.append(x[i])
        x_ss.append(x[i]+dx[i]/2)
    x_ss.append(x[-1])
    x_ss = np.array(x_ss)
    f_ss = np.interp(x_ss,x,f)
    return f_ss, x_ss

def multi_super_sample(f,x,runs):
    
    for i in range(runs):
        f,x = super_sample(f,x)
        
    return f,x

def mode(f):
    
    def counts(f):
        table = collections.Counter(iter(f)).most_common()
        if not table:
            return table
        maxfreq = table[0][1]
        for i in range(1, len(table)):
            if table[i][1] != maxfreq:
                table = table[:i]
                break
        return table
    
    table = counts(f)
    
    return table[0][0]

def grad_curvature(f,x):
    
    dy = grad_derivative(f,x,1)
    ddy = grad_derivative(f,x,2)
    k = np.zeros_like(f)
    for i in range(f.size):
        k[i] = abs(ddy[i])/(1 + dy[i]**2)**1.5
        
    return k, x

def grad_derivative(f,x,n):
    
    dy = f
    for i in range(n):
        dy = np.gradient(dy)/np.gradient(x)
        
    return dy

def diff_derivative(f,x,n):
    
    for i in range(n):
        dx = np.zeros(x.size - 1)
        for i in range(x.size - 1):
            dx[i] = (x[i+1] + x[i])/2
        dy = np.diff(f)/np.diff(x)
        f = dy
        x = dx

    return dy, dx
        
def diff_curvature(f,x):
    
    dy,dx = diff_derivative(f,x,1)
    ddy,ddx = diff_derivative(f,x,2)
    dy = interp1d(dx,dy)
    dy = dy(ddx)
    k = np.zeros_like(ddy)
    for i in range(ddx.size):
        k[i] = abs(ddy[i])/(1 + dy[i]**2)**1.5
    x_k = ddx
    
    return k, x_k

def norm_erf(arr,side):
    
    #side = 1 or -1
    x = np.linspace(-np.pi, np.pi, arr.size)
    x_erf = np.zeros_like(arr)
    for i in range(arr.size):
        x_erf[i] = (m.erf(x[i])+1)/2*arr[i*side]
        
    return x_erf

def norm_sup_gauss(arr,a,n):
    
    x = np.linspace(-np.pi**(1/n), np.pi**(1/n), arr.size)
    x_sg = np.zeros_like(arr)
    for i in range(arr.size):
        x_sg[i] = np.exp(-.5*(x[i]/a)**(2*n)) * arr[i]
        
    return x_sg

def power_2(x):
    
    i = 1
    while len(x) // 2**i > 0:
        i += 1
        
    return i

def midpoint(f):
    
    f_mid = np.zeros((len(f)-1))
    for i in range(len(f)-1):
        f_mid[i] = np.mean((f[i],f[i+1]))
        
    return f_mid

def linear_regression2line(linreg,x):
    
    def line(linreg,x):
        return linreg[0]*x + linreg[1]
    
    x_line = np.array([np.nanmin(x),np.nanmax(x)])        
    y_line = np.array([line(linreg,x_line[0]),line(linreg,x_line[1])])
    
    return x_line, y_line

def windowed_mean(f,x,N):
    
    f = np.array(f)
    x = np.array(x)
    wm = np.array([])
    wmx = np.array([])
    i = x[0]
    
    while i < x[-1]:
        ind = []
        for j in range(len(x)):
            if i <= x[j] < i + N:
                ind.append(j)
        wm = np.append(wm,np.nanmean(f[ind]))
        wmx = np.append(wmx,i + N/2)
        i += N
        
    return wmx, wm