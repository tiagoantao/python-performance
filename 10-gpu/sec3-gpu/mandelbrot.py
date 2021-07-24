from math import ceil
from numba import cuda
import numpy as np
from PIL import Image

size = 2000
start = -1.5, -1.3
end = 0.5, 1.3


@cuda.jit(device=True)
def compute_point(c):
    i = -1
    z = complex(0, 0)
    while abs(z) < 2:
        i += 1
        if i == 255:
            break
        z = z**2 + c
    return 255 - (255 * i)


@cuda.jit
def compute_all_points_doesnt_work(start, end, size, img_array):
    x, y = cuda.grid(2)
    if x >= img_array.shape[0] or y >= img_array.shape[1]:
        return
    mandel_x = (end[0] - start[0])*(x/size) + start[0]
    mandel_y = (end[1] - start[1])*(y/size) + start[1]
    img_array[y, x] = compute_point(complex(mandel_x, mandel_y))


@cuda.jit
def compute_all_points(startx, starty, endx, endy, size, img_array):
    x, y = cuda.grid(2)
    if x >= img_array.shape[0] or y >= img_array.shape[1]:
        return
    mandel_x = (end[0] - startx)*(x/size) + startx
    mandel_y = (end[1] - starty)*(y/size) + starty
    img_array[x, y] = compute_point(complex(mandel_x, mandel_y))


img_array = np.empty((size, size), dtype=np.uint8)
threads_per_block_2d = 16, 16
blocks_per_grid_2d = ceil(size / 16), ceil(size / 16)

compute_all_points[blocks_per_grid_2d, threads_per_block_2d](start[0], start[1], end[0], end[1], size, img_array)

img = Image.fromarray(img_array, mode="P")
img.save("mandelbrot.png")
