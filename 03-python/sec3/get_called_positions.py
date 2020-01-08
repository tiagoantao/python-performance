import sys
import zarr

from zarr import blosc

sys.path.insert(0, '../shared')

from utilities import PLINK_PREF
from ch3 import conv_chrom

root = zarr.open('ignore.zarr', mode='r')
positions = root['/chromosome-1/positions']
print(positions[:10])
