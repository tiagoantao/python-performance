import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

table_chunks = pd.read_csv(
    "../../07-pandas/sec1-intro/yellow_tripdata_2020-01.csv.gz",
    chunksize=1000000
    )
print(type(table_chunks))
for chunk in table_chunks:
    print(type(chunk))
    print(chunk.shape)


table_chunks = pd.read_csv(
    "../../07-pandas/sec1-intro/yellow_tripdata_2020-01.csv.gz",
    chunksize=1000000,
    dtype={
        "VendorID": float,  # We need to type
        "passenger_count": float,
        "RatecodeID": float,
        "PULocationID": float,
        "DOLocationID": float,
        "payment_type": float,
    }
)  # we need to reopen again

first = True
writer = None
for chunk in table_chunks:
    chunk_table = pa.Table.from_pandas(chunk)
    schema = chunk_table.schema
    if first:
        first = False
        writer = pq.ParquetWriter("output.parquet", schema=schema)
    writer.write_table(chunk_table)
writer.close()
pf = pq.ParquetFile("output.parquet")
pf.metadata
pf.num_row_groups
for groupi in range(pf.num_row_groups):
    group = pf.read_row_group(groupi)
    print(type(group), len(group))
    break
table = pf.read()
len(table)
table = pq.read_table("output.parquet")
