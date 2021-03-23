#cython: language_level=3
import numpy as np

cimport cython
cimport numpy as cnp


@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
@cython.cdivision(True)  # XXXXX
cdef cnp.float64_t get_tip_mean_cython_impl(
        cnp.float64_t[:] df_total,
        cnp.float64_t[:] df_tip) nogil:
    cdef cnp.float64_t frac_tip
    cdef int array_size = df_total.shape[0]
    cdef cnp.float64_t result = 0
    for i in range(array_size):
        result += df_tip[i] / df_total[i]
    return result / array_size


def get_tip_mean_cython(df_total, df_tip):
    return get_tip_mean_cython_impl(df_total, df_tip)
