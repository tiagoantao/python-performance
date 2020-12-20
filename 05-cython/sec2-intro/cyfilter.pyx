# cython: linetrace=True, language_level=3
import numpy as np

# cimport cython
cimport numpy as cnp


def darken_naive(image, darken_filter):
    nrows, ncols, _rgb_3 = image.shape
    dark_image = np.empty(shape=(nrows, ncols), dtype=np.uint8)
    for row in range(nrows):
        for col in range(ncols):
            pixel = image[row, col]
            mean = np.mean(pixel)
            dark_pixel = darken_filter[row, col]
            dark_image[row, col] = int(mean * (255 - dark_pixel) / 255)
    return dark_image


# def fails():
#     return a + 1


def darken_annotated(
        cnp.ndarray[cnp.uint8_t, ndim=3] image,
        cnp.ndarray[cnp.uint8_t, ndim=2] darken_filter):
    cdef int nrows = image.shape[0]  # Explain
    cdef int ncols = image.shape[1]
    cdef cnp.uint8_t dark_pixel
    cdef cnp.uint8_t mean  # define here
    cdef cnp.ndarray[cnp.uint8_t] pixel


    cdef cnp.ndarray[cnp.uint8_t, ndim=2] dark_image = np.empty(shape=(nrows, ncols), dtype=np.uint8)
    for row in range(nrows):
        for col in range(ncols):
            pixel = image[row, col]
            mean = (pixel[0] + pixel[1] + pixel[2]) // 3
            dark_pixel = darken_filter[row, col]
            dark_image[row, col] = mean * (255 - dark_pixel) // 255
    return dark_image
# TYPE everything
# You can do types more general


def darken_ufun():
    pass


def darken_gil(pixel, dark):
    mean = np.mean(pixel)
    return int(mean * (255 - dark) / 255)


# Explain reasons why one might want to do ufuns: broacast, etc
