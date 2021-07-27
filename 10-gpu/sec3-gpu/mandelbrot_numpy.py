from numba import vectorize, cuda
import numpy as np
from PIL import ImagePalette, Image

size = 2000
start = -1.5, -1.3
end = 0.5, 1.3


def compute_point_255_fn(c):
    i = -1
    z = complex(0, 0)
    while abs(z) < 2:
        i += 1
        if i == 255:
            break
        z = z**2 + c
    return 255 - (255 * i) // 255


compute_point_vectorized = vectorize(["uint8(complex128)"], target="cuda")(compute_point_255_fn)


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
