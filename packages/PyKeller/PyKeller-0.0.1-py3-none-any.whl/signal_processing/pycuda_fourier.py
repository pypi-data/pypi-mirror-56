#Fourier Analysis and Transform functions written with PyCuda

import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule

def reduce_exp_temp_ft(w,n,exp): #use this function to parallel reduce summate wavelet integrals
  
    mod = SourceModule(source = """
                                __global__ void reduce(float *exp, float *temp_ft){
                                extern __shared__ float temp[];

                                temp[threadIdx.x] = exp[threadIdx.x + blockDim.x * blockIdx.y + gridDim.y * blockDim.x * blockIdx.x];

                                __syncthreads();
                                
                                for(int t = 1; t < blockDim.x; t *= 2){
                                        if(threadIdx.x % (2 * t) == 0){
                                                temp[threadIdx.x] += temp[threadIdx.x + t];
                                        }
                                        __syncthreads();
                                }
                                        
                                if(threadIdx.x == 0){
                                        temp_ft[blockIdx.y + gridDim.y * blockIdx.x] = temp[0];
                                        
                                }
                                
                                } 
                                """)
    
    reduce = mod.get_function("reduce")
    
#    ft = np.zeros(w.size,dtype=np.float32)
#    y = int(np.ceil(np.log(t.size)/np.log(2))) #4*2**y
    temp_ft = np.zeros(w.size*n,dtype=np.float32)
    
    reduce(drv.In(exp), drv.Out(temp_ft), block = (1024,1,1), grid = (w.size,n,1), shared = (1024*4))
    
    return temp_ft

def reduce_temp_ft_ft(w,n,temp_ft): #use this function to parallel reduce summate wavelet integrals

    mod = SourceModule(source = """
                                __global__ void reduce(float *temp_ft, float *ft){
                                extern __shared__ float temp[];

                                temp[threadIdx.x] = temp_ft[threadIdx.x + blockDim.x * blockIdx.x];

                                __syncthreads();
                                
                                for(int t = 1; t < blockDim.x; t *= 2){
                                        if(threadIdx.x % (2 * t) == 0){
                                                temp[threadIdx.x] += temp[threadIdx.x + t];
                                        }
                                        __syncthreads();
                                }
                                        
                                if(threadIdx.x == 0){
                                        ft[blockIdx.x] = temp[0];
                                        
                                }
                                
                                } 
                                """)
    
    reduce = mod.get_function("reduce")
    
    ft = np.zeros(w.size,dtype=np.float32)
    y = int(np.ceil(np.log(n)/np.log(2)))
    
    reduce(drv.In(temp_ft), drv.Out(ft), block = (n,1,1), grid = (w.size,1,1), shared = (4*2**y))
    
    return ft

def ft(s,t): #runs the fourier transform

    w = np.linspace(1/(t[-1]-t[0]),1/(2*(t[1] - t[0])),s.size,dtype=np.float32)*2*np.pi
    
    s,n = gridize(s,1024)
    t,_ = gridize(t,1024)
    
    t = np.array(t).astype(np.float32)
    s = np.array(s).astype(np.float32)
 
    exp_real = fill_ft_real(s,t,w,n)
    exp_imag = fill_ft_imag(s,t,w,n)
    
    temp_ft_real = reduce_exp_temp_ft(w,n,exp_real)
    temp_ft_imag = reduce_exp_temp_ft(w,n,exp_imag)
    
    ft_real = reduce_temp_ft_ft(w,n,temp_ft_real)
    ft_imag = reduce_temp_ft_ft(w,n,temp_ft_imag)
    
    ft = ft_real + ft_imag * 1j
    
    return ft, w

def fill_ft_real(s,t,w,n): #use this function to multiply the function by the euler identity function

    mod = SourceModule(source = """
                                __global__ void fill(float *s, float *t, float *w, float *exp_real){
                                int s_index = threadIdx.x + blockDim.x * blockIdx.y;
                                int ft_index = s_index + gridDim.y * blockDim.x * blockIdx.x;                                
                                exp_real[ft_index] = s[s_index] * cos(w[blockIdx.x] * t[s_index]);
                                }
                                """)
    
    fill = mod.get_function("fill")
    
    exp_real = np.zeros(w.size*t.size).astype(np.float32)
      
    fill(drv.In(s), drv.In(t), drv.In(w), drv.Out(exp_real), block = (1024,1,1), grid = (w.size,n,1))

    return exp_real

def fill_ft_imag(s,t,w,n): #use this function to multiply the function by the euler identity function

    mod = SourceModule(source = """
                                __global__ void fill(float *s, float *t, float *w, float *exp_imag){
                                int s_index = threadIdx.x + blockDim.x * blockIdx.y;
                                int ft_index = s_index + gridDim.y * blockDim.x * blockIdx.x;
                                exp_imag[ft_index] = s[s_index] * -sin(w[blockIdx.x] * t[s_index]);
                                }
                                """)
    
    fill = mod.get_function("fill")
    
    exp_imag = np.zeros(w.size*t.size).astype(np.float32)
      
    fill(drv.In(s), drv.In(t), drv.In(w), drv.Out(exp_imag), block = (1024,1,1), grid = (w.size,n,1))

    return exp_imag

def gridize(x,N):
    
    n = int(np.ceil(x.size/N))
    x = np.append(x,np.zeros(N-x.size%N))
    
    return x, n