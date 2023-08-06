#Atmospheric Refractivity functions

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def N_eq(P,T,e): #refractivity of the atmosphere
    #P is the atmospheric pressure; hPa or mb
    #T is the absolute temperature; K
    #e is the partial pressure of water vapor in the atmosphere; hPa or mb
    return 77.6*P/T + 3.73*10**5*e/T**2

def M_eq(N,z): #modified refractivity of the atmosphere; assumes the earth is flat
    #N is the refractivity
    #z is the vertical height
    return N + .157*z
    
def snell_interp(nz_arr,z_arr,z):
    
    nz = interp1d(z_arr,nz_arr)

    return nz(z)

def run_snell_forward_propagation(nz,z,z0,dx,phi):
    
    ori = np.sign(phi)
    x0 = 0
    theta0 = np.pi/2 - abs(phi)
    
    x_ray = [x0]
    z_ray = [z0]
    while z0 > z[0] and z0 < z[-1] and z0 != np.nan and x0 < 50000:
        x0,z0,theta0,ori = snell_forward_propagation(x0,dx,z0,theta0,ori,nz,z)
        x_ray.append(x0)
        z_ray.append(z0)
    
    return x_ray, z_ray
        
def snell_forward_propagation(x0,dx,z0,theta0,ori,nz,z):
    
    x1 = x0 + dx
    
    if theta0 == np.pi/2:
        if z0 + .1 > z[-1] or z0 - .1 < z[0]:
            return np.nan, np.nan, np.nan, np.nan
    
        n0 = snell_interp(nz,z,z0 - .1)
        n1 = snell_interp(nz,z,z0 + .1)
        theta1 = abs(np.arcsin(n0/n1))
        if n0/n1 < 1:
            ori = -1
            return x1, z0, theta1, ori
        
        elif n0/n1 > 1:
            ori = 1
            return x1, z0, theta1, ori
        
        else:
            ori = 0
            theta1 = np.pi/2
            return x1, z0, theta1, ori
        
    dz = ori*np.tan(theta0)**-1*dx
    z1 = z0 + dz
    
    if z1 > z[-1] or z1 < z[0]:
        return np.nan, np.nan, np.nan, np.nan
    
    n0 = snell_interp(nz,z,z0)
    n1 = snell_interp(nz,z,z1)
    
    if n0*np.sin(theta0)/n1 == 1:
        theta1 = np.pi/2
        ori = -1
        return x1, z1, theta1, ori
    
    elif n0*np.sin(theta0)/n1 > 1:
        theta1 = theta0
        ori = -1
        return x1, z1, theta1, ori
    
    theta1 = np.arcsin(n0*np.sin(theta0)/n1)
    
    return x1, z1, theta1, ori

def snell_ray_trace(nz,zi,z0,dx):
    
    phi = np.linspace(np.pi/1024,-np.pi/1024,1024)

    rays = []
    ray_distance = []
    
    for i in range(len(phi)):
        
        x,z = run_snell_forward_propagation(nz,zi,z0,dx,phi[i])

        x = np.array(x)
        z = np.array(z)
        rays.append(z)
        ray_distance.append(x)
    
    ray_length = 0
    for i in rays:
        if ray_length < len(i):
            ray_length = len(i)
    
    for i in range(len(rays)):
        ray_length_diff = ray_length - rays[i].size
        nan_fill = np.empty(ray_length_diff)
        nan_fill.fill(np.nan)
        rays[i] = np.append(rays[i],nan_fill)
        ray_distance[i] = np.append(ray_distance[i],nan_fill)

    return rays, ray_distance
    
def snell_ray_trace_plot(rays,ray_distance):
    
    for i in range(len(rays)):
        plt.plot(ray_distance[i],rays[i])
    
    plt.show()
        
def potential_mirage(rays):
    
    mirage = False
    i = 0
    while i < len(rays) - 1:
        if True in list((rays[i+1] - rays[i]) > 0):
            mirage = True
            i = len(rays)
        i += 1
        
    return mirage