#Created: Wed May 29 20:46:29 2019
#By: mach

import numpy as np
import os
os.chdir('..')
os.chdir('..')
import PyKeller.signal_processing.pycuda_fourier as pyft

class Velocity:
    
    def __init__(self):
        self.raw = []
        self.turbulence = []
        self.wind = []
    
    def add_raw(self,u,v,w,T,t):
        raw = Raw(u,v,w,T,t)
        self.raw = raw
        
    def add_turbulence(self,u,v,w,T,t,period):
        turbulence = Turbulence(u,v,w,T,t,period)
        self.turbulence.append(turbulence)
    
    def add_wind(self,speed,theta,phi,period):
        wind = Wind(speed,theta,phi,period)
        self.wind.append(wind)
        
class Raw:
            
    def __init__(self,u,v,w,T,t):
        self.u = u
        self.v = v
        self.w = w
        self.T = T
        self.t = t
        
class Turbulence:
    
    def __init__(self,u,v,w,T,t,period):
        self.period = period
        self.u_mean, self.u_prime = run_reynolds_decomposition(u)
        self.v_mean, self.v_prime = run_reynolds_decomposition(v)
        self.w_mean, self.w_prime = run_reynolds_decomposition(w)
        self.T_mean, self.T_prime = run_reynolds_decomposition(T)
        self.t_mean, _ = run_reynolds_decomposition(t)

class Wind:
    
    def __init__(self,speed,theta,phi,period):
        self.period = period
        self.speed = speed
        self.direction = theta
        self.inclination = phi

def get_velocity(u,v,w,T,t):
    velocity = Velocity()
    velocity.add_raw(u,v,w,T,t)
    return velocity
    
def get_turbulence_wind(velocity,period):
    temp = []
    for i in [velocity.raw.u,velocity.raw.v,velocity.raw.w,velocity.raw.T,velocity.raw.t]:
        temp.append(periodize(i,velocity.raw.t,period))
    u = temp[0]
    v = temp[1]
    w = temp[2]
    T = temp[3]
    t = temp[4]
    u,v,w,theta,phi = run_tilt_correction(u,v,w)
    speed = run_wind_speed(u,v,w)
    velocity.add_turbulence(u,v,w,T,t,period)
    velocity.add_wind(speed,theta,phi,period)
        
def periodize(x,t,period):
    #period is in minutes, assuming t is in seconds
    Ts = t[1] - t[0]
    L = int(round(period*60/Ts))
    x_period = []
    for i in range(t.size//L):
        x_period.append(x[i*L:i*L+L])
    return x_period

def reynolds_decomposition(x):
    x_mean = np.nanmean(x)
    x_prime = x - x_mean
    return x_mean, x_prime

def run_reynolds_decomposition(x):
    #input periodized u, v, w
    x_mean = []
    x_prime = []
    for i in range(len(x)):
        temp_mean,temp_prime = reynolds_decomposition(x[i])
        x_mean.append(temp_mean)
        x_prime = np.append(x_prime,temp_prime)
    x_mean = np.array(x_mean)
    return x_mean, x_prime

def wind_speed(u,v,w):
    return (u**2 + v**2 + w**2)**.5

def run_wind_speed(u,v,w):
    #input periodized u, v, w
    wind = []
    for i in range(len(u)):
        wind.append(wind_speed(np.nanmean(u[i]),np.nanmean(v[i]),np.nanmean(w[i])))
    return wind

def wind_direction(u,v):
    return np.arctan2(v,u) #radians

def wind_inclination(u,w):
    return np.arctan2(w,u) #radians

def tilt_correction(u,v,w):
    u_mean,_ = reynolds_decomposition(u)
    v_mean,_ = reynolds_decomposition(v)
    w_mean,_ = reynolds_decomposition(w)
    theta = wind_direction(u_mean,v_mean)
    u = u * np.cos(theta) + v * np.sin(theta)
    v = -u * np.sin(theta) + v * np.cos(theta)
    u_mean,_ = reynolds_decomposition(u)
    phi = wind_inclination(u_mean,w_mean)
    u = u * np.cos(phi) + w * np.sin(phi)
    w = -u * np.sin(phi) + w * np.cos(phi)
    return u, v, w, theta, phi  

def run_tilt_correction(u,v,w):
    #input periodized u, v, w
    theta = np.zeros(len(u))
    phi = np.zeros_like(theta)
    for i in range(theta.size):
        u[i], v[i], w[i], theta[i], phi[i] = tilt_correction(u[i],v[i],w[i])
    return u, v, w, theta, phi

def turbulent_spectral_energy(x,t):
    x_ft,x_w = pyft.ft(x,t)
    energy = np.zeros_like(x_ft)
    for i in range(energy.size):
        energy[i] = 2*(x_ft[i].real**2 + x_ft[i].imag**2)
    return energy,x_w