from functools import partial
import sys
sys.path.insert(0, '.')
sys.path.insert(0, '../shared')
import time
from typing import List, IO

import psutil
import numpy as np
import zarr
from zarr.hierarchy import Group
from zarr import blosc

from utilities import MAX_POSITIONS, NUM_SAMPLES, PLINK_PREF, ZARR_DB
from ch2 import conv_chrom, encode_alleles

blosc.set_nthreads(1)
proc = psutil.Process()

print('block_size\tnum_threads\twall_time\tuser_time\tio_wait')
for block_size in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
    for num_threads in [1, 2, 4, 8]:
        root = zarr.open('ignore.zarr', mode='w')
        blosc.set_nthreads(num_threads)
        start_cpu = proc.cpu_times()
        start_time = time.time()
        conv_chrom(f'{PLINK_PREF}.tped', block_size, MAX_POSITIONS, root, 1)
        end_cpu = proc.cpu_times()
        end_time = time.time()
        wall_time = end_time - start_time
        user_time = end_cpu.user - start_cpu.user
        io_time = end_cpu.iowait - start_cpu.iowait
        print(f'{block_size}\t{num_threads}\t{wall_time}\t{user_time}\t{io_time}')
#memory size
# number of runs - we are doing only 1
