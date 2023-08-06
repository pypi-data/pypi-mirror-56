# Cuda Library
from numba import cuda
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
from math import sqrt
import numpy as np
from array import array
import pandas as pd

drv.init()
mod = SourceModule("""
__global__ void cuda_var1(double *a,double b, double *c,double *d, int N)
{ 
  extern __shared__ double sharedMem[1024];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){ 
    if(a[i]>-9999.0) sharedMem[threadIdx.x]+=(a[i]-b)*(a[i]-b)*d[i];
  }
   
   __syncthreads();
   
   for(int offset=blockDim.x/2;offset>0;offset>>=1){
      if(threadIdx.x<offset){
      sharedMem[threadIdx.x]+=sharedMem[threadIdx.x+offset];
      }
      __syncthreads();
   }
   if(threadIdx.x==0){
      c[blockIdx.x]=sharedMem[0];
   }
   
}
""")
cuda_var1 = mod.get_function("cuda_var1")


def cuda_var(nump1, nump2, mean_vec, yl):
    leng1, ncol = nump1.shape
    result = np.zeros((ncol, 1))
    weight_np = np.zeros((ncol, 1))
    nThreads = 1024
    nBlocks = 68
    c1 = np.zeros((68, 1))

    for i in range(0, ncol):
        input_num = np.float64(nump1[:, i].copy(order='C'))
        weight_np = np.float64(nump2.copy(order='C'))
        N = np.int32(leng1)
        mean1 = mean_vec[i]
        cuda_var1(drv.InOut(input_num), mean1, drv.InOut(c1), drv.InOut(
            weight_np), N, block=(nThreads, 1, 1), grid=(nBlocks, 1))
        result[i] = sum(c1)*leng1/((leng1-1)*yl)
    return(result)