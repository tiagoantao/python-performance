import dask
from dask.base import get_scheduler
import dask.dataframe as dd


df = dd.read_csv("FY2016-STC-Category-Table.csv")
print(get_scheduler(collections=[df]).__module__)

