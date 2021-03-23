import pandas as pd
import numpy as np

import pyximport

pyximport.install(
    setup_args={
        'include_dirs': np.get_include()})

import traversing_cython_impl as cy_impl  # noqa: E472

df = pd.read_csv("../sec1-intro/yellow_tripdata_2020-01.csv.gz")

df = df[(df.total_amount != 0)]

df_total = df["total_amount"].to_numpy()
df_tip = df["tip_amount"].to_numpy()

get_tip_mean_cython = cy_impl.get_tip_mean_cython
# get_tip_mean_cython(df_total, df_tip)
