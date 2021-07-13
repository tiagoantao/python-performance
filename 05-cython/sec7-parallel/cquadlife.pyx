#cython: language_level=3
import numpy as np

cimport cython
cimport numpy as cnp
from cython.parallel import prange


def create_random_world(y, x):
    cdef cnp.ndarray [cnp.uint8_t, ndim=2] world = np.random.randint(0, 5, (y, x), np.uint8)
    return world


@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
cdef void get_extended_world(
        cnp.uint8_t[:,:] world,
        cnp.uint8_t[:,:] extended_world) nogil:
    cdef int y = world.shape[0]
    cdef int x = world.shape[1]
    extended_world[1:y+1, 1:x+1] = world  # -1

    extended_world[0, 1:x+1] = world[y-1, :]  # top  -1 again
    extended_world[y+1, 1:x+1] = world[0, :]  # bottom
    extended_world[1:y+1, 0] = world[:, x-1]  # left
    extended_world[1:y+1, x+1] = world[:, 0]  # right

    extended_world[0, 0] = world[y-1, x-1]   # top left
    extended_world[0, x+1] = world[y-1, 0]   # top right
    extended_world[y+1, 0] = world[0, x-1]   # bottom left
    extended_world[y+1, x+1] = world[0, 0]   # bottom right


@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.wraparound(False)
cdef void live_core(
    cnp.uint8_t[:,:] old_world,
    cnp.uint8_t[:,:] extended_world,
    cnp.uint8_t[:,:] new_world,
    cnp.uint8_t[:] states) nogil:
    cdef cnp.uint32_t x, y, i
    cdef cnp.uint8_t num_alive, max_represented
    cdef int size_y = old_world.shape[0]
    cdef int size_x = old_world.shape[1]
    get_extended_world(old_world, extended_world)

    for x in prange(size_x):
        for y in range(size_y):
            for i in range(5):
                states[i] = 0
            for i in range(3):
                states[extended_world[y, x + i]] += 1
                states[extended_world[y + 2, x + i]] += 1
            states[extended_world[y + 1, x]] += 1
            states[extended_world[y + 1, x + 2]] += 1

            num_alive = states[1] + states[2] + states[3] + states[4]
            if num_alive < 2 or num_alive > 3:  # Too few or too many neighbors
                new_world[y, x] = 0
            elif old_world[y, x] != 0:  # Stays alive
                new_world[y, x] = old_world[y, x]
            elif num_alive == 3:  # Will be born
                max_represented = max(states[1], max(states[2], max(states[3], states[4])))
                if max_represented > 1:  # majority rule
                    for i in range(1, 5):
                        if states[i] == max_represented:
                            new_world[y, x] = i
                            break
                else:  # diversity - whichever doesn't exist
                    for i in range(1, 5):
                        if states[i] == 0:
                            new_world[y, x] = i
                            break
            else:
                new_world[y, x] = 0  # stays dead


def live(cnp.ndarray[cnp.uint8_t, ndim=2] old_world):
    cdef int size_y = old_world.shape[0]
    cdef int size_x = old_world.shape[1]
    cdef cnp.ndarray[cnp.uint8_t, ndim=2] extended_world = np.empty((size_y + 2, size_x + 2), dtype=np.uint8)   # empty
    cdef cnp.ndarray[cnp.uint8_t, ndim=2] new_world = np.empty((size_y, size_x), np.uint8)
    cdef cnp.ndarray[cnp.uint8_t, ndim=1] states = np.empty((5,), np.uint8)

    live_core(old_world, extended_world, new_world, states)
    return new_world
