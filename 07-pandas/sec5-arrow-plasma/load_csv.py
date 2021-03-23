import os
import sys

import pyarrow as pa
from pyarrow import csv
import pyarrow.plasma as plasma

csv_name = sys.argv[1]
client = plasma.connect("/tmp/fast_python")

convert_options = csv.ConvertOptions(
    column_types={
        "VendorID": pa.bool_()
    },
    true_values=["Y", "1"],
    false_values=["N", "2"])
table = csv.read_csv(
    csv_name,
    convert_options=convert_options
    )

pid = os.getpid()

plid = plasma.ObjectID(f"csv-{pid}".ljust(20, " ").encode("us-ascii"))

a = client.put(table, plid)  # eviction
