import os

import blosc
import numpy as np
# sync; echo 3 > /proc/sys/vm/drop_caches
# https://www.tecmint.com/clear-ram-memory-cache-buffer-and-swap-space-on-linux/

random_arr = np.random.randint(256, size=(1024, 1024, 1024)).astype(np.uint8)
a.dtype
a.size

zero_arr = np.zeros(shape=(1024, 1024, 1024)).astype(np.uint8)
rep_tile_arr = rep_cycle_arr = np.tile(
    np.arange(256).astype(np.uint8),
    4*1024*1024).reshape(1024,1024,1024)



def write_numpy(arr, prefix):
    np.save(f"{prefix}.npy", arr)
    os.system("sync")


def write_blosc(arr, prefix, cname="lz4"):
    b_arr = blosc.pack_array(arr, cname=cname)
    w = open(f"{prefix}.bl", "wb")
    w.write(b_arr)
    w.close()
    os.system("sync")


def read_numpy(prefix):
    return np.load(f"{prefix}.npy")


def read_blosc(prefix):
    r = open(f"{prefix}.bl", "rb")
    b_arr = r.read()
    r.close()
    return blosc.unpack_array(b_arr)

    
os.system("sync")
%time write_numpy(zero_arr, "zero")
%time write_blosc(zero_arr, "zero")
%time write_numpy(rep_tile_arr, "rep_tile")
%time write_blosc(rep_tile_arr, "rep_tile")
%time write_numpy(random_arr, "random")
%time write_blosc(random_arr, "random")

# Cache drop

%time _ = read_numpy("zero")
%time _ = read_blosc("zero")
%time _ = read_numpy("one")
%time _ = read_blosc("one")
%time _ = read_numpy("random")
%time _ = read_blosc("random")


# size fraction



# different algorithms

%time write_blosc(rep_tile_arr, "rep_tile")
%time _ = read_blosc("rep_tile")
%time write_blosc(rep_tile_arr, "rep_tile_zstd", "zstd")
%time _ = read_blosc("rep_tile_zstd")

# ^^^ size fraction (again)


# shift
for shuffle in [blosc.SHUFFLE, blosc.BITSHUFFLE, blosc.NOSHUFFLE]:
        a = blosc.pack_array(rep_tile_arr, shuffle=shuffle)
        print(len(a))
a = blosc.pack_array(rep_tile_arr, shuffle=blosc.BITSHUFFLE)
len(a)
a = blosc.pack_array(rep_tile_arr, shuffle=blosc.NOSHUFFLE)
len(a)

# timeit of pack

blosc.set_nthreads(16)
%timeit blosc.pack_array(rep_tile_arr, shuffle=blosc.SHUFFLE)
%timeit blosc.pack_array(rep_tile_arr, shuffle=blosc.NOSHUFFLE)
%timeit blosc.pack_array(rep_tile_arr, cname="zstd")
%timeit rep_tile_arr.copy()

blosc.detect_number_of_cores()
# memcpy
