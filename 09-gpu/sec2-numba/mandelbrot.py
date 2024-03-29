from numba import jit, prange
import numpy as np
from PIL import Image


def compute_point(c, max_iter=200):
    i = -1
    z = complex(0, 0)
    while abs(z) < 2:
        i += 1
        if i == max_iter:
            break
        z = z**2 + c
    return 255 - (255 * i) // max_iter


compute_point_numba = jit()(compute_point)
compute_point_numba_forceobj = jit(forceobj=True)(compute_point)
compute_point_numba(complex(4, 4))
compute_point_numba_forceobj(complex(4, 4))

size = 2000
start = -1.5, -1.3
end = 0.5, 1.3

img_array = np.empty((size, size), dtype=np.uint8)


def do_all(size, start, end, img_array, compute_fun):
    startx, starty = start
    endx, endy = end
    for xp in range(size):
        x = (endx - startx)*(xp/size) + startx  # precision issues
        # x = (xp - size/2) / (size/4)   # precision issues
        # print(x)
        for yp in range(size):
            y = (endy - starty)*(yp/size) + starty  # precision issues
            img_array[yp, xp] = compute_fun(complex(x,y))


do_all(size, start, end, img_array, compute_point_numba)
img = Image.fromarray(img_array, mode="P")
img.save("mandelbrot.png")
# img.putpalette(ImagePalette.sepia())

# compute_point_typed = jit(compute_point, "uint8(complex128)", nopython=True)


@jit(nopython=True, parallel=True, nogil=True)
def pdo_all(size, start, end, img_array, compute_fun):
    startx, starty = start
    endx, endy = end
    for xp in prange(size):
        x = (endx - startx)*(xp/size) + startx  # precision issues
        # x = (xp - size/2) / (size/4)   # precision issues
        # print(x)
        for yp in range(size):  # put prange here?
            # Loops are fine with Numba
            y = (endy - starty)*(yp/size) + starty  # precision issues
            b = complex(0, 0)
            b = compute_fun(complex(x, y))
            img_array[yp, xp] = b


# parallel_diagnostics - just note

# print(threading_layer())
