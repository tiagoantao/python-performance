import numpy as np
import cupy as cp
from cupyx.time import repeat

size = 5000

my_matrix = cp.ones((size, size), dtype=cp.uint8)
print(type(my_matrix))
np_matrix = my_matrix.get()
print(type(np_matrix))  # can be sent to numpy dependent libraries

2 * my_matrix

2 * np_matrix

print(repeat(lambda : 2 * my_matrix, n_repeat=200))
