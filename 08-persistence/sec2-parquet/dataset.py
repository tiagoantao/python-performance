import os

from pyarrow import csv
import pyarrow.compute as pc
import pyarrow.parquet as pq

table = csv.read_csv(
    "../../07-pandas/sec1-intro/yellow_tripdata_2020-01.csv.gz")

# year_column = pd.Series(np.full(len(table), 2020))
# month_column = pd.Series(np.full(len(table), 1))
# table = table.append_column("year", pa.Array.from_pandas(year_column))
# table = table.append_column("month", pa.Array.from_pandas(month_column))

table = table.filter(pc.invert(table["VendorID"].is_null()))
table = table.filter(pc.invert(table["passenger_count"].is_null()))

pq.write_to_dataset(table, root_path="all.parquet", partition_cols=["VendorID", "passenger_count"])
all_data = pq.read_table("all.parquet/")
dataset = pq.ParquetDataset("all.parquet/")
dir(dataset)
dataset.pieces
ds_all_data = dataset.read()
data_dir = "all.parquet/VendorID=1/passenger_count=3"
parquet_fname = os.listdir(data_dir)[0]
v1p3 = pq.read_table(f"{data_dir}/{parquet_fname}")
print(v1p3)
