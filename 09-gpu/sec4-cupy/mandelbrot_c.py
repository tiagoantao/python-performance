from math import ceil

import numpy as np
import cupy as cp
from cupyx.time import repeat
from PIL import Image

size = 2000
start = -1.5, -1.3
end = 0.5, 1.3

cp_img_array = cp.empty((size, size), dtype=cp.uint8)


def prepare_pos_array(start, end, pos_array):
    size = pos_array.shape[0]
    startx, starty = start
    endx, endy = end
    for xp in range(size):
        x = (endx - startx)*(xp/size) + startx
        for yp in range(size):
            y = (endy - starty)*(yp/size) + starty 
            pos_array[yp, xp] = complex(x, y)


pos_array = np.empty((size, size), dtype=np.complex64)
prepare_pos_array(start, end, pos_array)

cp_pos_array = cp.array(pos_array)

threads_per_block = 16 ** 2
blocks_per_grid = ceil(size / 16) ** 2

c_compute_mandelbrot = cp.RawKernel(r'''
#include <cupy/complex.cuh>
extern "C" __global__
void raw_mandelbrot(const complex<float>* pos_array,
             char* img_array) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int i = -1;
    complex<float> z = complex<float>(0.0, 0.0);
    complex<float> c = pos_array[x];
    while (abs(z) < 2) {
        i++;
        if (i == 255) break;
        z = z*z + c;
    }
    img_array[x] = i;
}
''', 'raw_mandelbrot')
c_compute_mandelbrot((blocks_per_grid,) , (threads_per_block,), (cp_pos_array, cp_img_array))
img = Image.fromarray(cp.asnumpy(cp_img_array), mode="P")
img.save("cmandelbrot.png")


# print(repeat(
#     lambda: c_compute_mandelbrot((blocks_per_grid,) , (threads_per_block,), (cp_pos_array, cp_img_array)),
#     n_repeat=200))
