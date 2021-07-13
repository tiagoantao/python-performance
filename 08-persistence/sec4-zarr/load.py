import numpy as np
import zarr

# z = zarr.zeros((10000, 10000), chunks=(1000, 1000), dtype='i4')
genomes = zarr.open("/home/tantao/write/fast_python/plink/db.zarr")

a = list(genomes.groups())
gr2 = a[0][1]
dir(gr2)
genomes


genomes.tree()
type(genomes["chromosome-2"])
genomes["chromosome-2"].tree()
genomes["chromosome-2/calls"][:100,0]

list(genomes["chromosome-2"].groups())


def traverse_hierarchy(group, location=""):
    for name, array in group.arrays():
        print(f"{location}/{name} {array.shape} {array.dtype}")
    for name, group in group.groups():
        my_root = f"{location}/{name}"
        print(my_root + "/")
        traverse_hierarchy(group, my_root)


traverse_hierarchy(genomes)

in_chr_2 = genomes["chromosome-2"]
pos_chr_2 = genomes["chromosome-2/positions"]
calls_chr_2 = genomes["chromosome-2/calls"]
alleles_chr_2 = genomes["chromosome-2/alleles"]

print(in_chr_2.info)
print(pos_chr_2.info)
print(calls_chr_2.info)
print(alleles_chr_2.info)


big_array = zarr.create((10000, 10000),dtype=np.int64, chunks=(1000,1000))
big_array.size
dir(big_array)
big_array.chunks
big_array.store
# fsspec

# string arrays
