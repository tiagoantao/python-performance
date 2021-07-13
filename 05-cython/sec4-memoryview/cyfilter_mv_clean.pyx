# cython: language_level=3
# cython: linetrace=True
# cython: binding=True
import numpy as np
cimport cython
cimport numpy as cnp


@cython.boundscheck(False)
cdef void darken_annotated_mv(
        cnp.uint8_t[:,:,:] image_mv,
        cnp.uint8_t[:,:] darken_filter_mv,
        cnp.uint8_t[:,:] dark_image_mv) nogil:
    cdef int nrows = image_mv.shape[0]
    cdef int ncols = image_mv.shape[1]
    cdef cnp.uint8_t dark_pixel
    cdef cnp.uint8_t mean  # define here
    cdef cnp.uint8_t[:] pixel
    for row in range(nrows):
        for col in range(ncols):
            pixel = image_mv[row, col]
            mean = (pixel[0] + pixel[1] + pixel[2]) // 3
            dark_pixel = darken_filter_mv[row, col]
            dark_image_mv[row, col] = mean * (255 - dark_pixel) // 255


cpdef darken_annotated(
        cnp.ndarray[cnp.uint8_t, ndim=3] image,
        cnp.ndarray[cnp.uint8_t, ndim=2] darken_filter):
    cdef int nrows = image.shape[0]  # Explain
    cdef int ncols = image.shape[1]
    cdef cnp.ndarray[cnp.uint8_t, ndim=2] dark_image = np.empty(shape=(nrows, ncols), dtype=np.uint8)
    cdef cnp.uint8_t[:,:] dark_image_mv
    cdef cnp.uint8_t [:,:,:] image_mv
    cdef cnp.uint8_t[:,:] darken_filter_mv
    dark_image_mv = dark_image
    darken_filter_mv = darken_filter
    image_mv = image
    darken_annotated_mv(image_mv, darken_filter_mv, dark_image_mv)
    return dark_image


def blah():  # Has to be here
    pass
