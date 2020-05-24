#cython: language_level=3
import numpy as np

cimport cython
cimport numpy as np


def create_random_world(y, x):
    cdef np.ndarray [np.int_t, ndim=2] world = np.random.randint(0, 5, (y, x), np.int)
    return world


@cython.boundscheck(False)
@cython.nonecheck(False)
def get_extended_world(np.ndarray world):
    cdef int y = world.shape[0]
    cdef int x = world.shape[1]
    cdef np.ndarray[np.int_t, ndim=2] extended_world = np.empty((y + 2, x + 2), np.int)   # empty
    extended_world[1:-1, 1:-1] = world  # XXX broadcast

    extended_world[0, 1:-1] = world[-1, :]  # top
    extended_world[-1, 1:-1] = world[0, :]  # bottom
    extended_world[1:-1, 0] = world[:, -1]  # left 
    extended_world[1:-1, -1] = world[:, 0]  # right

    extended_world[0, 0] = world[-1, -1]   # top left
    extended_world[0, -1] = world[-1, 0]   # top right
    extended_world[-1, 0] = world[0, -1]   # bottom left
    extended_world[-1, -1] = world[0, 0]   # bottom right
    return extended_world


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def live(np.ndarray[np.int_t, ndim=2] old_world):
    cdef np.ndarray[np.int_t, ndim=2] extended_world = get_extended_world(old_world)
    cdef int size_y = old_world.shape[0]
    cdef int size_x = old_world.shape[1]
    cdef np.ndarray[np.int_t, ndim=2] new_world = np.empty((size_y, size_x), np.int)
    for x in range(size_x):
        for y in range(size_y):
            states = [0, 0, 0, 0, 0]
            for i in range(3):
                states[extended_world[y, x + i]] += 1
                states[extended_world[y + 2, x + i]] += 1
            states[extended_world[y + 1, x]] += 1
            states[extended_world[y + 1, x + 2]] += 1
            alive = states[1:]
            num_alive = sum(alive)
            if num_alive < 2 or num_alive > 3:  # Too few or too many neighbors
                new_world[y, x] = 0
            elif old_world[y, x] != 0:  # Stays alive
                new_world[y, x] = old_world[y, x]
            elif num_alive == 3:  # Will be born
                max_represented = max(alive)
                if max_represented > 1:  # majority rule
                    new_world[y, x] = 1 + alive.index(max_represented)
                else:  # diversity - whichever doesn't exist
                    new_world[y, x] = 1 + alive.index(0)
            else:
                new_world[y, x] = 0  # stays dead
    return new_world
