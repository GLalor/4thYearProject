import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy

a = numpy.random.randn(4,4) # 4x4 array of random numbers
a = a.astype(numpy.float32) # number format for card
a_gpu = cuda.mem_alloc(a.nbytes) # allocation of memory for card and cpu to use
cuda.memcpy_htod(a_gpu, a) # transfering the data to memeory location
# kernal code written in c++
mod = SourceModule(""" 
  __global__ void doublify(float *a)
  {
    int idx = threadIdx.x + threadIdx.y*4;
    a[idx] *= 2;
  }
  """)
func = mod.get_function("doublify") #calling compiling function
func(a_gpu, block=(4,4,1)) # passing array
a_doubled = numpy.empty_like(a) 
cuda.memcpy_dtoh(a_doubled, a_gpu) # retriving results
print(a_doubled)
print(a)