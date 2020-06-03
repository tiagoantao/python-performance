import zarr

from constants import ZARR_DB

root = zarr.open(ZARR_DB) # compare with size of plink file
root.info
root['/chromosome-1/calls'].info
zarr.tree(root)
