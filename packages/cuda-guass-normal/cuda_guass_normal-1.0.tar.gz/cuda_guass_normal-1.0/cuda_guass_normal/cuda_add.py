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
__global__ void cuda_add(double *a,double *c, int N)
{ 
  extern __shared__ double sharedMem[1024];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){
     if(a[i]>-9999.0) sharedMem[threadIdx.x]+=a[i];
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
cuda_add1 = mod.get_function("cuda_add")


def cuda_add(nump1):
    leng1 = len(nump1)
    nThreads = 1024
    nBlocks = 68
    c1 = np.zeros((68, 1))
    input_num = np.float64(nump1.copy(order='C'))
    N = np.int32(leng1)
    cuda_add1(drv.InOut(input_num), drv.InOut(c1), N,
              block=(nThreads, 1, 1), grid=(nBlocks, 1))
    result = sum(c1)
    return(result[0])