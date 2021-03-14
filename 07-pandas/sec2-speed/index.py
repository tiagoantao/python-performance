import pandas as pd
import numpy as np

df = pd.read_csv("../sec1-intro/yellow_tripdata_2020-01.csv.gz")

df.columns
df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

%timeit df[df["tpep_pickup_datetime"] == "2020-01-06 08:13:00"]  # 17.1 ms
df["tpep_pickup_datetime"].value_counts().head(2)
df["tpep_pickup_datetime"].value_counts().tail(2)
df_sort = df.sort_values("tpep_pickup_datetime")
%timeit df_sort[df_sort["tpep_pickup_datetime"] == "2020-01-06 08:13:00"]
%timeit df_sort[df_sort["tpep_dropoff_datetime"] == "2020-01-06 08:13:00"]
df_pickup = df.set_index("tpep_pickup_datetime")
df_pickup_sort = df_pickup.sort_index()
%timeit df_pickup.loc["2020-01-06 08:13:00"]
%timeit df_pickup_sort.loc["2020-01-06 08:13:00"]
%timeit df_pickup_sort.at["2020-01-06 08:13:00", "extra"]
%timeit df_pickup_sort.at["2020-01-29 06:20:33", "extra"]

%timeit df_sort[
    (df_sort["tpep_pickup_datetime"] >= "2020-01-06") &
    (df_sort["tpep_pickup_datetime"] <= "2020-01-08")]  # 52.7 ms
%timeit df_pickup_sort["2020-01-06":"2020-01-08")]  # 1ms


%timeit df[
    (df["tpep_pickup_datetime"] == "2020-01-06 08:13:00") &
    (df["congestion_surcharge"] > 0)]

my_time = df_pickup_sort.loc["2020-01-06 08:13:00"]
my_time[my_time["congestion_surcharge"] > 0]
