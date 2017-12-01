
import math

import numpy as np

from numba import cuda, jit
 
 
@jit('void(double[:], double[:], double, double, double, double[:])',
     target='gpu')
def step(last, paths, dt, c0, c1, normdist):
    i = cuda.grid(1)
    if i >= paths.shape[0]:
        return
    noise = normdist[i]
    paths[i] = last[i] * math.exp(c0 * dt + c1 * noise)
 