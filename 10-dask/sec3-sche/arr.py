from time import time

import numpy as np
import dask.array as da
from dask.distributed import Client
from PIL import Image

client = Client('127.0.0.1:8786')
#client = Client()

start = -1.5, -1.3
end = 0.5, 1.3


def prepare_pos_array(size, start, end, pos_array):
    size = pos_array.shape[0]
    startx, starty = start
    endx, endy = end
    for xp in range(size):
        x = (endx - startx)*(xp/size) + startx
        for yp in range(size):
            y = (endy - starty)*(yp/size) + starty
            pos_array[yp, xp] = complex(x, y)


def block_prepare_pos_array(size, pos_array):
    nrows, ncols = pos_array.shape
    ret = np.empty(shape=(nrows,ncols), dtype=np.complex128)
    startx, starty = start
    endx, endy = end
    
    for row in range(nrows):
        x = (endx - startx) * ((pos_array[row, 0] // size ) / size) + startx
        for col in range(ncols):
            y = (endy - starty) * ((pos_array[row, col] % size) / size) + starty
            ret[row, col] = complex(x, y)
    return ret


def compute_point(c):
    i = -1
    z = complex(0, 0)
    max_iter = 200
    while abs(z) < 2:
        i += 1
        if i == max_iter:
            break
        z = z**2 + c
    return 255 - (255 * i) // max_iter


size = 3
pos_array = da.empty((size, size), dtype=np.complex128)
prepare_pos_array(3, start, end, pos_array)
pos_array.visualize("10-size3.png", rankdir="LR")
# pos_array.persist()

size = 1000
# pos_array = da.empty((size, size), dtype=np.int64)
range_array = da.arange(0, size*size).reshape(size, size)
range_array
range_array = range_array.rechunk(size // 2, size // 2)
range_array.visualize("10-rechunk.png", rankdir="TB")
range_array = range_array.persist()
range_array
#pos_array.chunks
#pos_array.npartitions
#pos_array.chunks
#pos_array[0].shape
#pos_array.blockwise()
# block_prepare_pos_array(3, np.array([0,1,2,3,4,5,6,7,8]).reshape(3,3))
pos_array = da.blockwise(
    lambda x: block_prepare_pos_array(size, x),
    'ij', range_array, 'ij', dtype=np.complex128)
pos_array.visualize("10-blockwise.png", rankdir="TB")
pos_array = pos_array.persist()  # scheduler="single-threaded")
pos_array.size
pos_array.nbytes

u_compute_point = da.frompyfunc(compute_point, 1, 1)

image_arr = u_compute_point(pos_array)
image_arr.visualize("10-image_arr.png", rankdir="TB")
image_np = image_arr.compute().astype(np.uint8)
image = Image.fromarray(image_np, mode="P")
image.save("mandelbrot.png")


def time_scenario(size, persist_range, persist_pos, chunk_div=10):
    start_time = time()
    size = size
    range_array = da.arange(0, size*size).reshape(size, size).persist()
    range_array = range_array.rechunk(size // chunk_div, size // chunk_div)
    range_array = range_array.persist() if persist_range else range_array
    pos_array = da.blockwise(
        lambda x: block_prepare_pos_array(size, x),
        'ij', range_array, 'ij', dtype=np.complex128)

    pos_array = pos_array.persist() if persist_pos else pos_array
    image_arr = u_compute_point(pos_array)
    # image_arr.visualize("xx.png", rankdir="TB")
    image_arr.compute()
    return time() - start_time


for size in [500, 1000, 5000, 10000]:  # for size in [10000]:
    print()
    for persist_range in [False, True]:
        for persist_pos in [False, True]:
            client.restart()
            print(size, persist_range, persist_pos,
                  time_scenario(size, persist_range, persist_pos))

5000/7000

size = 500
print(size, False, False, 2, time_scenario(size, False, False, 2))

size = 5000
client = Client('127.0.0.1:8786')
client = client.restart()
print(size, False, False, 10, time_scenario(size, True, True, 10))

size = 500
print(size, False, False, 2, time_scenario(size, False, False, 2))
print(size, False, False, time_scenario(size, False, False))
print(size, True, True, time_scenario(size, True, True))

size = 1000
for chunk_div in [1, 2, 4, 10, 100]:
    client.restart()
    print(size, False, False, chunk_div, time_scenario(size, False, False, chunk_div))
    client.restart()
    print(size, True, True, chunk_div, time_scenario(size, True, True, chunk_div))


size = 10000
print(size, False, False, time_scenario(size, False, False))
client.restart()
print(size, True, True, time_scenario(size, True, True))
