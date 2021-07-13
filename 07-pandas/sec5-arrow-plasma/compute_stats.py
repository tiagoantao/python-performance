import time

import pandas as pd
import pyarrow as pa
from pyarrow import csv
import pyarrow.compute as pc
import pyarrow.plasma as plasma

client = plasma.connect("/tmp/fast_python")
while True:
    client = plasma.connect("/tmp/fast_python")
    all_objects = client.list()

    for plid, keys in all_objects.items():
        plid_str = ""
        try:
            plid_str = plid.binary().decode("us-ascii")
        except UnicodeDecodeError:
            continue
        if plid_str.startswith("csv-"):
            original_pid = plid_str[4:]
            result_plid = plasma.ObjectID(
                f"result-{original_pid}".ljust(20, " ")[:20].encode("us-ascii"))
            if client.contains(result_plid):
                continue
            print(f"Working on: {plid_str}")
            table = client.get(plid)
            t0 = table.filter(
                pc.not_equal(table["total_amount"], 0.0))
            my_mean = pc.mean(
                pc.divide(t0["tip_amount"], t0["total_amount"])).as_py()
            result_plid = plasma.ObjectID(
                f"result-{original_pid}".ljust(20, " ")[:20].encode("us-ascii"))
            client.put(my_mean, result_plid)
    time.sleep(0.05)
