from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List

import zarr
from zarr.hierarchy import Group

# XXX This will be done with queues?

PLINK_PREF = 'my_hapmap'
ZARR_DB = 'db.zarr'
NUM_WORKERS = 2  # XXX set as number of cores


def get_samples(pref: str) -> List[str]:
    pass


def conv_chrom(zarr_db: Group, chrom: int) -> None:
    pass


zarr_db = zarr.open(ZARR_DB, mode='w')
conv_chrom_in_db = partial(conv_chrom, zarr_database='sdASd')
my_promises = {}
with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    my_promises = {executor.submit(conv_chrom_in_db, chrom=chrom)
                   for chrom in range(1, 23)}
zarr_db.close()
