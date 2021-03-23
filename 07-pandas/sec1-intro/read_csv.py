import pandas as pd
import numpy as np

df = pd.read_csv("yellow_tripdata_2020-01.csv")
df = pd.read_csv("yellow_tripdata_2020-01.csv.gz")
df.info(memory_usage="deep")

def summarize_columns(df):
    for c in df.columns:
        print(c, df[c].dtype, len(df[c].unique()),
              df[c].memory_usage(deep=True) // (1024**2), sep="\t")


summarize_columns(df)

df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
summarize_columns(df)
df.info(memory_usage="deep")

# vvv -> Will fail
df["payment_type"] = df["payment_type"].astype(np.int8)

df["payment_type"] = df["payment_type"].fillna(0).astype(np.int8)
df["fare_amount_32"] = df["fare_amount"].astype(np.float32)
(df["fare_amount_32"] - df["fare_amount"]).abs().sum()

# vvv -> Will fail
df["store_and_fwd_flag"].value_counts(dropna=False)
df["store_and_fwd_flag"] = df["store_and_fwd_flag"].apply(ord)

df["store_and_fwd_flag"] = df["store_and_fwd_flag"].fillna(" ").apply(ord).apply(
    lambda x: [32, 78, 89].index(x) - 1).astype(np.int8)
df["store_and_fwd_flag"]
df = pd.read_csv(
    "yellow_tripdata_2020-01.csv.gz",
    dtype={
        "VendorID": np.int8,
        "trip_distance": np.float16,
        "PULocationID": np.uint8,
        "DOLocationID": np.uint8,
        },
    parse_dates=[
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"],
    converters={
       "VendorID":
           lambda x: np.int8(["", "1", "2"].index(x)),
        "store_and_fwd_flag":
           lambda x: ["", "N", "Y"].index(x) - 1,
        "payment_type":
           lambda x: -1 if x == "" else int(x),
        "RatecodeID":
           lambda x: -1 if x == "" else int(x),
        "passenger_count":
           lambda x: -1 if x == "" else int(x)

    }
)
df.info(memory_usage="deep")
for c in df.columns:
    if df[c].dtype == np.float64:
        df[c] = df[c].astype(np.float16)
    if df[c].dtype == np.int64:
        df[c] = df[c].astype(np.int8)

df.info(memory_usage="deep")
for c in df.columns:
    cnts = df[c].value_counts(dropna=False)
    if len(cnts) < 10:
        print()
        print(cnts)

df = pd.read_csv(
    "yellow_tripdata_2020-01.csv.gz",
    dtype={
        "congestion_surcharge": np.float16,
        },
    parse_dates=[
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"],
    usecols=[
        "congestion_surcharge",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"],
)
df.info(memory_usage="deep")
