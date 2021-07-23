from numba import cuda
import numpy as np


def double_not_this(my_array):
    for position in range(my_array):
        my_array[position] *= 2


@cuda.jit
def double(my_array):
    position = cuda.grid(1)
    my_array[position] *= 2


my_array = np.ones(1000)
double(my_array)

threads_per_block = 20
blocks_per_grid = 50

my_array = np.ones(1000)
double[blocks_per_grid, threads_per_block](my_array)
assert (my_array == 2).all()

threads_per_block = 16
blocks_per_grid = 63

my_array = np.ones(1000)
double[blocks_per_grid, threads_per_block](my_array)
assert (my_array == 2).all()

@cuda.jit
def double_safe(my_array):
    position = cuda.grid(1)
    if position > my_array.shape[0]:
        return
    my_array[position] *= 2


my_array = np.ones(1000)
double_safe[blocks_per_grid, threads_per_block](my_array)
assert (my_array == 2).all()


@cuda.jit
def double_safe_explicit(my_array):
    position = cuda.blockIdx * cuda.blockDim.x + cuda.threadIdx.x
    if position > my_array.shape[0]:
        return
    my_array[position] *= 2


my_array = np.ones(1000)
double_safe_explicit[blocks_per_grid, threads_per_block](my_array)
assert (my_array == 2).all()


@cuda.jit
def double_matrix(my_array):
    x = cuda.blockIdx * cuda.blockDim.x + cuda.threadIdx.x
    y = cuda.blockIdx * cuda.blockDim.y + cuda.threadIdx.y
    # x, y= cuda.grid(2)
    if x > my_array.shape[0]:
        return
    if y > my_array.shape[1]:
        return
    my_array[x, y] *= 2


threads_per_block_2d = 16, 16
blocks_per_grid_2d = 63, 63

my_matrix = np.ones((1000, 1000))
double_matrix[blocks_per_grid_2d, threads_per_block_2d](my_matrix)
assert (my_matrix == 2).all()
