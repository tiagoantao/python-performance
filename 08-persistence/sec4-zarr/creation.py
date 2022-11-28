from functools import partial
from multiprocessing import Pool

import numpy as np
import zarr

# z = zarr.zeros((10000, 10000), chunks=(1000, 1000), dtype='i4')
genomes = zarr.open("/home/tantao/write/fast_python/plink/db.zarr")


chrom_sizes = []
for chrom in range(1, 23):
    chrom_pos_array = genomes[f"chromosome-{chrom}/positions"]
    chrom_sizes.append(chrom_pos_array.shape[0])

total_size = sum(chrom_sizes)

CHUNK_SIZE = 20000
all_calls = zarr.open(
    "all_calls.zarr", "w",
    shape=(total_size, 210),
    dtype=np.uint8,   # type change
    chunks=(CHUNK_SIZE,))  # refer the MB recommendation
# refer nested

# ls inside
print(all_calls.info)


def do_serial():
    curr_pos = 0
    for chrom in range(1, 23):
        chrom_calls_array = genomes[f"chromosome-{chrom}/calls"]
        my_size = chrom_calls_array.shape[0]
        all_calls[curr_pos: curr_pos + my_size, :] = chrom_calls_array
        curr_pos += my_size


do_serial()
print(all_calls.info)


def process_chunk(genomes, all_calls, chrom_sizes, chunk_size, my_chunk):
    all_start = my_chunk * chunk_size
    remaining = all_start
    chrom = 0
    chrom_start = 0
    for chrom_size in chrom_sizes:
        chrom += 1
        remaining -= chrom_size
        if remaining <= 0:
            chrom_start = chrom_size + remaining
            remaining = -remaining
            break
    while remaining > 0:
        write_from_chrom = min(remaining, CHUNK_SIZE)
        remaining -= write_from_chrom
        chrom_calls = genomes[f"chromosome-{chrom}/calls"]
        all_calls[all_start:all_start + write_from_chrom, :] = chrom_calls[chrom_start: chrom_start + write_from_chrom, :]
        all_start = all_start + write_from_chrom


#        if write_from_chrom < chunk_size and chrom != 22:
#            from_next_chrom = chunk_size - write_from_chrom
#            chrom_calls = genomes[f"chromosome-{chrom+1}/calls"]
#            new_all_start = all_start + write_from_chrom
#            all_calls[new_all_start:new_all_start + from_next_chrom, :] = chrom_calls[: from_next_chrom, :]


partial_process_chunk = partial(process_chunk, genomes, all_calls, chrom_sizes, CHUNK_SIZE)


#for i in range(all_calls.nchunks):
#    print(i)
#    partial_process_chunk(i)


def do_parallel():
    with Pool() as p:
        p.map(partial_process_chunk, range(all_calls.nchunks))


# all_calls[-1::]
