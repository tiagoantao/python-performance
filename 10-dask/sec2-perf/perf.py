import numpy as np
import dask.dataframe as dd

taxes = dd.read_csv("FY2016-STC-Category-Table.csv", sep="\t")
taxes["year"] = taxes["Survey_Year"] - 2000
taxes.visualize(filename="10-single.png", rankdir="LR")#, collapse_output=True)
taxes = dd.read_csv("FY2016-STC-Category-Table.csv", sep="\t", blocksize=5000)
taxes["year"] = taxes["Survey_Year"] - 2000
taxes.visualize(filename="10-block.png", rankdir="LR")#, collapse_output=True)
taxes["Amount"] = taxes["Amount"].str.replace(",", "").replace("X", np.nan).astype(float)
taxes = taxes.persist()
taxes.visualize(filename="10-persist.png", rankdir="LR")#, collapse_output=True)
taxes["k_amount"] = taxes["Amount"] / 1000
taxes.visualize(filename="10-k.png", rankdir="LR")#, collapse_output=True)
max_k = taxes["k_amount"].max()
max_k.visualize(filename="10-max_k.png", rankdir="LR")#, collapse_output=True)
taxes = taxes.persist()
sv = taxes.sort_values("k_amount")
sv.visualize(filename="10-sv.png", rankdir="LR")
print(sv.compute())
taxes = taxes.persist()
gb = taxes.groupby("Geo_Name")
gb[["k_amount"]].max().visualize(filename="10-gb.png", rankdir="LR")
taxes = taxes.persist()
taxes2 = taxes.repartition(npartitions=2)
taxes2.visualize(filename="10-repart.png", rankdir="LR")
taxes = taxes.persist()
print(taxes.index)
taxes.iloc[:, 0]
taxes.compute()
taxes.known_divisions
print(1, taxes.divisions)
# taxes = taxes.set_index(["Geo_Name", "Tax_Type"])
taxes = taxes.set_index(["Geo_Name"])
print(taxes.npartitions)
print(taxes.divisions)
taxes2 = taxes.repartition(divisions=["Alabama", "New Hampshire", "Wyoming"])
print(taxes2.npartitions)
print(taxes2.divisions)
print(taxes2.partitions)
taxes2.to_csv("partial-*.csv")
taxes2.to_parquet("taxes2.parquet")

from pyarrow import parquet
taxes2_pq = parquet.read_table("taxes2.parquet")
taxes_pd = taxes2_pq.to_pandas()
