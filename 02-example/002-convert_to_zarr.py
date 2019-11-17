from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
# Consider the multiprocessing module on the relevant chapter (vs futures)
from functools import partial, lru_cache
import os
from typing import List, IO

import numpy as np
import zarr
from zarr.hierarchy import Group

# XXX This could be done with queues?

PLINK_PREF = 'my_hapmap'
ZARR_DB = 'db.zarr'
NUM_WORKERS = os.cpu_count()
NUM_WORKERS = 4
# XXX set as number of cores?
# XXX consider set affinity


def get_samples(pref: str) -> List[str]:
    with open(f'{pref}.tfam') as tfam:
        return map(lambda line: line.split(' ')[1],
                   tfam.readlines())


def place_stream_start(stream: IO[str], chrom: int) -> None:
    stream.seek(0)
    if chrom == 1:
        return
    current_position = 0
    for line in stream:
        if int(line.split(' ')[0]) == chrom:
            stream.seek(current_position)
            return
        current_position += len(line)
# we can do this way better as we will see later


def encode_alleles(a1: str, a2: str, code: List[str]) -> int:
    if a1 == '0' or a2 == '0':
        return 3
    if a1 == a2:
        return 1
    if a1 == code[0]:
        return 0
    return 2


def conv_chrom_slow(tfam: IO[str], num_samples: int,
               root: Group, chrom: int) -> None:
    chrom_group = root.create_group(f'chromosome-{chrom}')
    place_stream_start(tfam, chrom)
    positions = []
    all_calls = chrom_group.array('calls', [], dtype='u8')
    for line in tfam:
        tokens = line.rstrip().split(' ')
        line_chrom = int(tokens[0])
        if chrom != line_chrom:
            break
        positions.append(int(tokens[3]))
        calls = tokens[4:]
        alleles = list(set(calls[4:]) - set([0]))
        variant_calls = []
        for sample in range(num_samples):
            a1, a2 = calls[2 * sample: 2 * sample + 2]
            variant_calls.append(encode_alleles(a1, a2, alleles))
        all_calls.append(np.array(variant_calls))
        if len(positions) > 2000:
            print(positions[-1])
            break
    #all_calls.reshape
    chrom_group.array('positions', positions)


def conv_chrom(fname: str, num_samples: int,
               root: Group, chrom: int) -> None:
    tfam = open(fname)  # We need to open each time, so that seeks are different for parallel executions
    print(chrom)
    chrom_group = root.create_group(f'chromosome-{chrom}')

    positions = []
    place_stream_start(tfam, chrom)
    for line in tfam:
        tokens = line.rstrip().split(' ')
        line_chrom = int(tokens[0])
        if chrom != line_chrom:
            break
        positions.append(int(tokens[3]))
    chrom_group.array('positions', positions)

    all_calls = chrom_group.zeros('calls', shape=(len(positions), num_samples), dtype='u8')
    place_stream_start(tfam, chrom)
    for count, line in enumerate(tfam):
        tokens = line.rstrip().split(' ')
        calls = tokens[4:]
        alleles = list(set(calls[4:]) - set([0]))
        for sample_position, sample in enumerate(range(num_samples)):
            a1, a2 = calls[2 * sample: 2 * sample + 2]
            all_calls[count, sample_position] = encode_alleles(a1, a2, alleles)
        if count % 10000 == 0:
            print(chrom, count)
        if count % 50000 == 49999:
            break
    #all_calls.reshape


root = zarr.open(ZARR_DB, mode='w')

samples = np.array(get_samples(PLINK_PREF), dtype='str')
root.array('samples', samples)
num_samples = samples.size

conv_chrom_in_db = partial(conv_chrom, f'{PLINK_PREF}.tped', num_samples, root)
my_promises = {}
#a = conv_chrom_in_db(open(f'{PLINK_PREF}.tped'), chrom=1)
#We should consider a threadpoolexecutor
with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
    results = executor.map(conv_chrom_in_db,
                           [chrom for chrom in range(1, 23)])
    list(results)

#root.close()

# Note: open of tped has to occur 22 times to avoid stream confusion

#snakeviz
#pyflame


# create and then recompress?


# Times (2 chroms, upto 100_000 positions):
#
# Single thread 2.55, 2.30, 0.25
# Dual thread 2.22, 3.11, 0.41
# Dual proc 1.64 3.08, 0.32

# 22 chroms, up to 50_000
# Single thread 31.55 29.19 2.25
# 2 thread      29.37 34.2 4.43
# 2 proc        22.33 39.28 3.32
# 8 thread      32.05 43.29 8.45
# 8 proc        15.12 95.34 7.42

# Linux time is really good (extra info)

# Profile slow version

# Profile multithreaded/multiprocess version to find the cullprit


# Paralelizzable because CPU bound (zarr) -  re-assess in the Zarr chapter

# print tree and compression rate of a chrom

# try with no zarr compression

# do read with asyncio?
