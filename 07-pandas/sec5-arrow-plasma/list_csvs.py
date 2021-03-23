import pyarrow as pa
import pyarrow.plasma as plasma

client = plasma.connect("/tmp/fast_python")

all_objects = client.list()

for plid, keys in all_objects.items():
    try:
        plid_str = plid.binary().decode("us-ascii")
    except UnicodeDecodeError:
        continue
    if plid_str.startswith("csv-"):
        print(plid_str, plid)
        print(keys)
    elif plid_str.startswith("result-"):
        print(plid_str, plid)
        print(keys)
