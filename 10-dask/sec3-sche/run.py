import sys
from pprint import pprint
import numpy as np
import dask.dataframe as dd
from dask.distributed import Client

client = Client('127.0.0.1:8786')
print(client)
scheduler = client.scheduler
for what, instances in client.get_versions().items():
    print(what)
    if what == 'workers':
        for name, instance in instances.items():
            print(name)
            pprint(instance)
    else:
        pprint(instances)
#client.restart()
#taxes = dd.read_csv("FY2016-STC-Category-Table.csv", sep="\t", blocksize=5000)
#taxes.persist()

#worker_names = list(client.get_versions()["workers"].keys())
#worker_names

# client.restart()
taxes = dd.read_csv("FY2016-STC-Category-Table.csv", sep="\t", blocksize=8000)
taxes["year"] = taxes["Survey_Year"] - 2000
taxes.visualize(filename="10-single.png", rankdir="LR")#, collapse_output=True)
taxes = dd.read_csv("FY2016-STC-Category-Table.csv", sep="\t", blocksize=5000)
taxes["year"] = taxes["Survey_Year"] - 2000
taxes["Amount"] = taxes["Amount"].str.replace(",", "").replace("X", np.nan).astype(float)
taxes = taxes.persist()
sys.exit(1)
taxes["k_amount"] = taxes["Amount"] / 1000
max_k = taxes["k_amount"].max()
taxes = taxes.persist()

sv = taxes.sort_values("k_amount")
taxes = taxes.persist()
gb = taxes.groupby("Geo_Name")
gb[["k_amount"]].max().visualize(filename="10-gb.png", rankdir="LR")
taxes = taxes.persist()
taxes2 = taxes.repartition(npartitions=2)
taxes = taxes.persist()
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

