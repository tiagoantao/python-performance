import os

PLINK_PREF = 'my_hapmap'
ZARR_DB = 'db.zarr'
NUM_WORKERS = os.cpu_count() // 2  # Is this cores, processors or threads?
