# cython: profile=True
import numpy as np

cimport cython
cimport numpy as cnp


@cython.profile(True)
def darken_annotated(
        cnp.ndarray[cnp.uint8_t, ndim=3] image,
        cnp.ndarray[cnp.uint8_t, ndim=2] darken_filter):
    cdef int nrows = image.shape[0]  # Explain
    cdef int ncols = image.shape[1]
    cdef cnp.uint8_t dark_pixel
    cdef cnp.uint8_t mean  # define here
    cdef cnp.ndarray[cnp.uint8_t] pixel

    cdef cnp.ndarray[cnp.uint8_t, ndim=2] dark_image = np.empty(shape=(nrows, ncols), dtype=np.uint8)
    for i in range(1000000):
        i = i + 1 - 1
    for row in range(nrows):
        for col in range(ncols):
            pixel = image[row, col]
            mean = (pixel[0] + pixel[1] + pixel[2]) // 3
            dark_pixel = darken_filter[row, col]
            dark_image[row, col] = mean * (255 - dark_pixel) // 255
    return dark_image
