from math import ceil

import numpy as np
import cupy as cp
from cupyx.time import repeat
from numba import cuda
from PIL import Image

size = 2000
start = -1.5, -1.3
end = 0.5, 1.3


@cuda.jit
def compute_all_mandelbrot(startx, starty, endx, endy, size, img_array):
    x, y = cuda.grid(2)
    if x >= img_array.shape[0] or y >= img_array.shape[1]:
        return
    mandel_x = (end[0] - startx)*(x/size) + startx
    mandel_y = (end[1] - starty)*(y/size) + starty
    c = complex(mandel_x, mandel_y)
    i = -1
    z = complex(0, 0)
    while abs(z) < 2:
        i += 1
        if i == 255:
            break
        z = z**2 + c
    img_array[y, x] = i


threads_per_block_2d = 16, 16
blocks_per_grid_2d = ceil(size / 16), ceil(size / 16)

cp_img_array = cp.empty((size, size), dtype=cp.uint8)

compute_all_mandelbrot[blocks_per_grid_2d, threads_per_block_2d](
    start[0], start[1],
    end[0], end[1],
    size, cp_img_array)

# print(repeat(
#     lambda: compute_all_mandelbrot[blocks_per_grid_2d, threads_per_block_2d](
#         start[0], start[1], end[0], end[1], size, cp_img_array),
#     n_repeat=200))

img = Image.fromarray(cp.asnumpy(cp_img_array), mode="P")
img.save("imandelbrot.png")
