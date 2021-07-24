from numba import vectorize, cuda
import numpy as np
from PIL import ImagePalette, Image

size = 2000
start = -1.5, -1.3
end = 0.5, 1.3


@cuda.jit
def compute_point_255_fna(pos_array, img_array):
    x, y = cuda.grid(2)
    if x >= pos_array.shape[0] or y >= pos_array.shape[1]:
        return
    c = pos_array[x, y]
    i = -1
    z = complex(0, 0)
    while abs(z) < 2:
        i += 1
        if i == 255:
            break
        z = z**2 + c
    img_array[x, y] = 255 - (255 * i) // 255


@cuda.jit("uint8(complex128)", device=True, inline=True)
def compute_point_255_fn(c):
    i = -1
    z = complex(0, 0)
    while abs(z) < 2:
        i += 1
        if i == 255:
            break
        z = z**2 + c
    return 255 - (255 * i) // 255


@vectorize("uint8(complex128)", target="cuda")
def compute_point_255(c):
    return compute_point_255_fn(c)


def prepare_pos_array(start, end, pos_array):
    size = pos_array.shape[0]
    startx, starty = start
    endx, endy = end
    for xp in range(size):
        x = (endx - startx)*(xp/size) + startx
        for yp in range(size):
            y = (endy - starty)*(yp/size) + starty 
            pos_array[yp, xp] = complex(x, y)


pos_array = np.empty((size, size), dtype=np.complex128)

img_array = np.empty((size, size), dtype=np.uint8)
