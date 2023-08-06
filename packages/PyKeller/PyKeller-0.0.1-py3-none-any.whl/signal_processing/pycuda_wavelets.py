#Wavelet Analysis and Transform functions written with PyCuda

import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule

def reduce_psi(x,a,b,psi): #use this function to parallel reduce summate wavelet integrals
  
    mod = SourceModule(source = """
                                __global__ void reduce(float *psi, float *wt){
                                extern __shared__ float temp[];
                                
                                int block_index = threadIdx.x + blockDim.x * (gridDim.y * blockIdx.x + blockIdx.y);
                                int grid_index = gridDim.y * blockIdx.x + blockIdx.y;

                                temp[threadIdx.x] = psi[block_index];

                                __syncthreads();
                                
                                for(int t = 1; t < blockDim.x; t *= 2){
                                        if(threadIdx.x % (2 * t) == 0){
                                                temp[threadIdx.x] += temp[threadIdx.x + t];
                                        }
                                        __syncthreads();
                                }
                                        
                                if(threadIdx.x == 0){
                                        wt[grid_index] = temp[0];
                                }
                                
                                } 
                                """)
    
    reduce = mod.get_function("reduce")
    
    wt = np.zeros((a.size*b.size)).astype(np.float32)
    y = int(np.ceil(np.log(x.size)/np.log(2)))
    
    reduce(drv.In(psi), drv.Out(wt), block = (x.size,1,1), grid = (a.size,b.size), shared = (4*2**y))
    
    return wt

def kwwt(f,x,a,b,n): #runs the wavelet transform with the "Keller" Wavelet (TM). Ha.
    
    x = np.array(x).astype(np.float32)
    a = np.array(a).astype(np.float32)
    b = np.array(b).astype(np.float32)
    n = np.array(n).astype(np.int16)
    f = np.array(f).astype(np.float32)
    
    psi_real, psi_imag = fill_kw(f,x,a,b,n)
    wt_real = reduce_psi(x,a,b,psi_real)
    wt_imag = reduce_psi(x,a,b,psi_imag)
    
    wt = wt_real + wt_imag * 1j
    
    return wt

def fill_kw(f,x,a,b,n): #use this function to multiply the function by the "Keller" wavelet function
  
    mod = SourceModule(source = """
                                __global__ void fill(float *f, float *x, float *a, float *b, int *n, float *psi_real, float *psi_imag){
                                int index = threadIdx.x + blockDim.x * (gridDim.y * blockIdx.x + blockIdx.y);
                                psi_real[index] = f[threadIdx.x] / pow(a[blockIdx.x], 0.5) * -sin(2 * 3.14159265359 * (x[threadIdx.x] - b[blockIdx.y]) / a[blockIdx.x]) * pow(0.01, pow(2 * (x[threadIdx.x] - b[blockIdx.y]) / a[blockIdx.x], 2 * n[0]));
                                psi_imag[index] = f[threadIdx.x] / pow(a[blockIdx.x], 0.5) * cos(2 * 3.14159265359 * (x[threadIdx.x] - b[blockIdx.y]) / a[blockIdx.x]) * pow(0.01, pow(2 * (x[threadIdx.x] - b[blockIdx.y]) / a[blockIdx.x], 2 * n[0]));
                                }
                                """)
    
    fill = mod.get_function("fill")
    
    psi_real = np.zeros(a.size*b.size*x.size).astype(np.float32)
    psi_imag = np.zeros(a.size*b.size*x.size).astype(np.float32)
      
    fill(drv.In(f), drv.In(x), drv.In(a), drv.In(b), drv.In(n), drv.Out(psi_real), drv.Out(psi_imag), block = (x.size,1,1), grid = (a.size,b.size))

    return psi_real, psi_imag

def sgwwt(f,x,a,b,n,y_a): #runs the wavelet transform with the super Gaussian Wavelet
    
    x = np.array(x).astype(np.float32)
    a = np.array(a).astype(np.float32)
    b = np.array(b).astype(np.float32)
    n = np.array(n).astype(np.int16)
    y_a = np.array(y_a).astype(np.float32)
    f = np.array(f).astype(np.float32)
    
    psi = fill_sgw(f,x,a,b,n,y_a)
    wt = reduce_psi(x,a,b,psi)
    
    wt = np.reshape(wt,(a.size,b.size))
    
    return wt

def fill_sgw(f,x,a,b,n,y_a): #use this function to multiply the function by the super Gaussian wavelet function
  
    mod = SourceModule(source = """
                                __global__ void fill(float *f, float *x, float *a, float *b, int *n, float *y_a, float *psi){
                                int index = threadIdx.x + blockDim.x * (gridDim.y * blockIdx.x + blockIdx.y);
                                psi[index] = f[threadIdx.x] / pow(a[blockIdx.x], 0.5) * pow(y_a[0], pow((x[threadIdx.x] - b[blockIdx.y]) * 2 / a[blockIdx.x], 2 * n[0]));
                                }
                                """)
                                                                    
    fill = mod.get_function("fill")
    
    psi = np.zeros(a.size*b.size*x.size).astype(np.float32)
      
    fill(drv.In(f), drv.In(x), drv.In(a), drv.In(b), drv.In(n), drv.In(y_a), drv.Out(psi), block = (x.size,1,1), grid = (a.size,b.size))

    return psi