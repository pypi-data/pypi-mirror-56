from numba import cuda
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

drv.init()

from .cuda_add import *
from .cuda_mean import *
from .cuda_var import *
from .cuda_correlation import *
from .guass_normal import *
from .cuda_cut import *

__version__ = '1.2'
