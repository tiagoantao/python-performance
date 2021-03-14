import pandas as pd
import numpy as np

df = pd.read_csv("../sec1-intro/yellow_tripdata_2020-01.csv.gz")

df.columns
df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])


df.tip_amount.value_counts()

df.iloc[0].iat[0]

df = df[(df.total_amount != 0)]
df_10 = df.sample(frac=0.1)
df_100 = df.sample(frac=0.01)

def get_tip_mean_explicit(df):  # df_100: 10s 
    all_tips = 0
    all_totals = 0
    for i in range(len(df)):
        row = df.iloc[i]
        all_tips += row["tip_amount"]
        all_totals += row["total_amount"]
    return all_tips / all_totals


def get_tip_mean_iterrows(df):  # df_100: 4s
    all_tips = 0
    all_totals = 0
    for i, row in df.iterrows():
        all_tips += row["tip_amount"]
        all_totals += row["total_amount"]
    return all_tips / all_totals


def get_tip_mean_itertuples(df):  # 18 s
    all_tips = 0
    all_totals = 0
    for my_tuple in df.itertuples():
        all_tips += my_tuple.tip_amount
        all_totals += my_tuple.total_amount
    return all_tips / all_totals


def get_tip_mean_apply(df): # df_10: 9.42s
    frac_tip = df.apply(
        lambda row: row["tip_amount"] / row["total_amount"],
        axis=1
    )
    return frac_tip.mean()


def get_tip_mean_apply2(df):  # df_10: 14.9s
    frac_tip = df.apply(
        lambda row: row.tip_amount / row.total_amount,
        axis=1
    )
    return frac_tip.mean()


def get_tip_mean_vector(df):  # 32 ms
    frac_tip = df["tip_amount"] / df["total_amount"]
    return frac_tip.mean()
