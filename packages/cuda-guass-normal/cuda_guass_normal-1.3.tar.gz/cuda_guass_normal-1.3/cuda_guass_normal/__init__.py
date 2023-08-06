from numba import cuda
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule



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





drv.init()
mod = SourceModule("""
__global__ void cuda_mean(double *a, double *c, double *d, int N)
{ 
  extern __shared__ double sharedMem[1024];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){
     if(a[i]>-9999.0) sharedMem[threadIdx.x]+=a[i]*d[i];
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
cuda_mean1 = mod.get_function("cuda_mean")




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




drv.init()
mod = SourceModule("""
__global__ void cuda_covar1(double *a,double b, double *c,double *d, double *e, double f, int N)
{ 
  extern __shared__ double sharedMem[1024];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){ 
    if(a[i]>-9999.0) sharedMem[threadIdx.x]+=(a[i]-b)*(e[i]-f)*d[i];
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
cuda_covar1 = mod.get_function("cuda_covar1")


drv.init()
mod=SourceModule("""
__global__ void cuda_cut(double *a, double *b, double *c,double thre, int N)
{ 
  extern __shared__ double sharedMem[1024];
  int index=threadIdx.x+blockIdx.x*blockDim.x;
  int stride=blockDim.x*gridDim.x;
  sharedMem[threadIdx.x]=0;
  for(int i=index;i<N;i=i+stride){
     if(a[i]>thre){
     sharedMem[threadIdx.x]+=b[i];
     }
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
cuda_cut1=mod.get_function("cuda_cut")


from .cuda_add import *
from .cuda_mean import *
from .cuda_var import *
from .cuda_correlation import *
from .guass_normal import *
from .cuda_cut import *

__version__ = '1.3'
