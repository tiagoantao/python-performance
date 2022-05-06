import pyarrow as pa
from pyarrow import csv
import pyarrow.compute as pc
import pyarrow.parquet as pq

table = csv.read_csv(
    "../../07-pandas/sec1-intro/yellow_tripdata_2020-01.csv.gz")
pq.write_table(table, "202001.parquet")


convert_options = csv.ConvertOptions(
    column_types={
        "VendorID": pa.uint8(),
        "passenger_count": pa.uint8(),
        })

table = csv.read_csv(
    "../../07-pandas/sec1-intro/yellow_tripdata_2020-01.csv.gz",
    convert_options=convert_options)
# vvv read_csv doesn't support this
table["VendorID"]

tp = table.to_pandas()

# pq.write_table(table, "202001.parquet", use_dictionary=False)
pq.write_table(table, "202001.parquet", )

#memory size, disk size
#retype as int64 for both
#memory size, disk size
# RLE example?

table = pq.read_table("202001.parquet")
# ^^^ time against readcsv
# Has metadata with it (unlike csv)

parquet_file = pq.ParquetFile("202001.parquet")

dir(parquet_file)
parquet_file.schema_arrow
metadata = parquet_file.metadata
print(metadata)
print(metadata.serialized_size)
type(metadata)
print(parquet_file.schema)
group = metadata.row_group(0)
print(group)
dir(group)
vendor_col = group.column(0)
print(vendor_col)
tip_col = group.column(13)
print(tip_col)
pq.write_table(table, "202001_std.parquet", compression="ZSTD")

print(len(table["tip_amount"].unique()))

silly_table = pa.Table.from_arrays([
    table["VendorID"],
    table["VendorID"].take(
        pc.sort_indices(table["VendorID"]))],
    ["unordered", "ordered"]
)

pq.write_table(silly_table, "silly.parquet")
silly = pq.ParquetFile("silly.parquet")
silly_group = silly.metadata.row_group(0)
print(silly_group.column(0))
print(silly_group.column(1))
silly_table["ordered"].unique()
tp["VendorID"].value_counts(dropna=False)

# reduce time from ms to s
# partitioned datasets
# rows groups (maybe with a single dataset)

len(tp.fare_amount.unique())
tp.columns
tp[tp.tpep_pickup_datetime.isna()]
