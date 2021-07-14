from numba import vectorize, cuda
import numpy as np
from PIL import ImagePalette, Image


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

