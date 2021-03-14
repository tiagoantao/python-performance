import pandas as pd
import numpy as np

df = pd.read_csv("../sec1-intro/yellow_tripdata_2020-01.csv.gz")

df.columns
df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])


df = df[(df.total_amount != 0)]

df_total = df["total_amount"].to_numpy()
df_tip = df["tip_amount"].to_numpy()

print(type(df_tip))


def get_tip_mean_numpy(df_total, df_tip):  # 11 ms
    frac_tip = df_total / df_tip
    return frac_tip.mean()


def get_tip_mean_numpy4(df_total, df_tip):
    frac_tip = df_total / df_tip + df_total / df_tip + df_total / df_tip + df_total / df_tip
    return frac_tip.mean()


def get_tip_mean_numexpr(df):
    return df.eval("tip_amount / total_amount", engine="numexpr").mean()


def get_tip_mean_numexpr4(df):
    return df.eval("tip_amount / total_amount + tip_amount / total_amount + tip_amount / total_amount + tip_amount / total_amount", engine="numexpr").mean()
