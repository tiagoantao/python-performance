# cython: language_level=3
import numpy as pn
cimport cython
cimport numpy as cnp


cdef void darken_pixel(
        cnp.uint8_t* image_pixel,
        cnp.uint8_t* darken_filter_pixel,
        cnp.uint8_t* dark_image_pixel) nogil:
    cdef cnp.uint8_t mean
    mean = (image_pixel[0] + image_pixel[1] + image_pixel[2]) // 3
    dark_image_pixel[0] = mean * (255 - darken_filter_pixel[0]) // 255

cnp.import_array()
cnp.import_ufunc()

cdef cnp.PyUFuncGenericFunction loop_func[1]
cdef char all_types[3]
cdef void *funcs[1]

loop_func[0] = cnp.PyUFunc_FF_F

all_types[0] = cnp.NPY_UINT8
all_types[1] = cnp.NPY_UINT8
all_types[2] = cnp.NPY_UINT8

funcs[0] = <void*>darken_pixel

darken = cnp.PyUFunc_FromFuncAndDataAndSignature(
    loop_func,
    funcs,
    all_types,
    1,
    2,
    1,
    0,
    "darken",
    "Darken a pixel",
    0, # unused
    "(n),()->()"
)
                                            