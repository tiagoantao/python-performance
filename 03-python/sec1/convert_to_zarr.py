import sys
import zarr

from zarr import blosc

sys.path.insert(0, '../shared')

from utilities import PLINK_PREF
from ch3 import conv_chrom

MAX_POSITIONS = 100000
BLOCK_SIZE = int(sys.argv[1])

blosc.set_nthreads(1)
root = zarr.open('db.zarr', mode='w')
for chrom in range(1, 23):
    print(f'Currently doing chromosome {chrom}')
    conv_chrom(f'{PLINK_PREF}.tped', BLOCK_SIZE, root, chrom)

#memory size
# number of runs - we are doing only 1
