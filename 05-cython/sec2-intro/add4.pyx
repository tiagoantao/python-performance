#cython: language_level=3


def add4(my_number):
    i = my_number + 4
    return i


def add4_annotated(int my_number):
    cdef int i
    i = my_number + 4
    return i


cdef int add4_annotated_cret(int my_number):
    return my_number + 4


cpdef int add4_annotated_cpret(int my_number):
    return add4_annotated_cret(my_number)
