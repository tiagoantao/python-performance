import pandas as pd
import numpy as np

df = pd.read_csv("yellow_tripdata_2020-01.csv")
df = pd.read_csv("yellow_tripdata_2020-01.csv.gz")
df.info(memory_usage="deep")


def summarize_columns(df):
    for c in df.columns:
        print(c, len(df[c].unique()),
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

df["store_and_fwd_flag"] =
df["store_and_fwd_flag"].fillna(" ").apply(ord).apply(lambda x: [32, 78, 89].index(x) - 1).value_counts()
