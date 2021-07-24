from numba import vectorize
import numpy as np
# from PIL import ImagePalette, Image


def compute_point(c, max_iter=200):
    i = -1
    z = complex(0, 0)
    while abs(z) < 2:
        i += 1
        if i == max_iter:
            break
        z = z**2 + c
    return 255 - (255 * i) // max_iter


compute_point_ufunc = vectorize(["uint8(complex128,uint64)"], target="parallel")(compute_point)

size = 2000
start = -1.5, -1.3
end = 0.5, 1.3


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
prepare_pos_array(start, end, pos_array)
