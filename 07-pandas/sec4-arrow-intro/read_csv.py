import pandas as pd
import pyarrow as pa
from pyarrow import csv

table = pd.read_csv("../sec1-intro/yellow_tripdata_2020-01.csv.gz")  # 12s
table = csv.read_csv("../sec1-intro/yellow_tripdata_2020-01.csv.gz")  # 2s

tot_bytes = 0
for name in table.column_names:
    col_bytes = table[name].nbytes
    col_type = table[name].type
    print(name, col_bytes // (1024 ** 2))
    tot_bytes += col_bytes
print("Total", tot_bytes // (1024 ** 2))

table["store_and_fwd_flag"].unique()

table_df = table.to_pandas()

convert_options = csv.ConvertOptions(
    column_types={
        "VendorID": pa.bool_(),
        # "trip_distance": pa.float16()
    },
    true_values=["Y", "1"],
    false_values=["N", "2"])
table = csv.read_csv(
    "../sec1-intro/yellow_tripdata_2020-01.csv.gz",
    convert_options=convert_options
    )
print(
    table["store_and_fwd_flag"].unique(),
    table["store_and_fwd_flag"].nbytes // (1024 ** 2),
    table["VendorID"].nbytes // 1024,
    table["store_and_fwd_flag"].nbytes // 1024
)

x = pa.array([False, True]).cast(pa.string()).cast(pa.bool_())

table_df = table.to_pandas()
print(table_df.store_and_fwd_flag)
mission_impossible = table.to_pandas(self_destruct=True)

import pyarrow.compute as pc
pc.equal(table["total_amount"], 0)
pc.equal(table["total_amount"], 0.0)
t0 = table.filter(
    pc.not_equal(table["total_amount"], 0.0))


pc.mean(pc.divide(t0["tip_amount"], t0["total_amount"])) # 18ms
# The fair comparison is (also do on other computer)
 
