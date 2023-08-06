#NASA MPLNET functions

import numpy as np
import os
os.chdir('..')
os.chdir('..')
import PyKeller.signal_processing.pycuda_wavelets as py_wv
import PyKeller.signal_processing.wavelets as wv
import PyKeller.signal_processing.signal_analysis as sa
import PyKeller.atmos_sci.met_analysis as ma
import matplotlib.pyplot as plt
from scipy import signal

def nrb_pad(nrb,z):
    nrb_padded = []
    for i in range(nrb[0,:].size):
        nrb_new,z_new = wv.padding_start_sg(nrb[:,i],z,337.4741,0.01,5) #337.4741 m is the height of the mpl above sea level
        nrb_padded.append(nrb_new)
    nrb_padded = np.transpose(np.array(nrb_padded))
    z_padded = z_new
    return nrb_padded,z_padded

def cuda_pbl_layers(nrb,z):
    res = z[1]-z[0]
    a = np.arange(4*res,z[18]+res,res) #change to an end point of about 4 km if the height array is limited
    if np.isnan(nrb[0]): #checking for nan filled nrb files
        return []
    wt = py_wv.kwwt(nrb,z,a,z,5)
    wt = wt.real
    wt = wv.clip_wavelet_kw(wt,a,z)
    pblh = pbl_layer(wt,z)
    return pblh
   
def pbl_layers(wt,b):
    wt = sa.moving_mean(wt[0,:],1)
    pks,_ = signal.find_peaks(wt)
    pks,_ = signal.find_peaks(wt,height=np.mean(wt[pks]))
    return pks
    
def pbl_layer(wt,b): #Just takes the max, seems to work really well
    wt = sa.moving_mean(wt[0,:],1)
    pks = np.where(wt==np.nanmax(wt))[0]
    if len(pks) > 0:
        return list(pks)
    else:
        return []

def pbl_layers_heights(pblh,z):
    k = 0
    for i in range(len(pblh)):
        if len(pblh[i]) > k:
            k = len(pblh[i])
    layers = np.empty((len(pblh),k))
    layers.fill(np.nan)
    for i in range(len(pblh)):
        for j in range(k):
            if j < len(pblh[i]):
                if not np.isnan(pblh[i][j]):
                    layers[i,j] = z[pblh[i][j]]
    return layers

def run_pbl_layers(nrb,z):
    z = z[0:46]
    nrb = nrb[0:46,:]
    nrb,z = nrb_pad(nrb,z)
    pblh = []
    for i in range(nrb[0,:].size):
        nrb_i = sa.moving_mean(nrb[:,i],1)
        pblh.append(cuda_pbl_layers(nrb_i,z))
    return nrb,z,pblh

def plot_nrb(nrb,z,t,t_div):
    st = ma.min_to_hour_min(t)
    plt.style.use('dark_background')
    plt.pcolormesh(t,z,nrb,cmap='gnuplot2',vmin=0,vmax=2,zorder=1)
    plt.xticks(t[0:t.size:t_div],st[0:t.size:t_div], rotation='vertical')
    plt.show()
    
def plot_nrb_layers(nrb,z,t,t_div,layers):
    for i in range(len(layers[0])):
        plt.scatter(t,layers[:,i],zorder=2)
    plot_nrb(nrb,z,t,t_div)