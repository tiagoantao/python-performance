import os
import zipfile

import fsspec
from fsspec.implementations.github import GithubFileSystem
from fsspec.implementations.local import LocalFileSystem
from fsspec.implementations.zip import ZipFileSystem
import pandas as pd

from pyarrow import csv
from pyarrow.fs import PyFileSystem, FSSpecHandler

git_user = "tiagoantao"
git_repo = "python-performance"

# fs = GithubFileSystem(git_user, git_repo)  # branch, ....
fs = LocalFileSystem()
os.chdir("../..")
# print(fs.ls(""))
#print(fs.ls("08-persistence/sec1-fsspec"))


def get_zip_list(fs, root_path=""):
    for root, dirs, fnames in fs.walk(root_path):
        for fname in fnames:
            if fname.endswith(".zip"):
                yield f"{root}/{fname}"


def get_zips(fs):
    for zip_name in get_zip_list(fs):
        fs.get_file(zip_name, "/tmp/dl.zip")
        yield zip_name


def describe_all_csvs_in_zips_0(fs):
    for zip_name in get_zips(fs):
        my_zip = zipfile.ZipFile("/tmp/dl.zip")
        print(zip_name)
        for zip_info in my_zip.infolist():
            if not zip_info.filename.endswith(".csv"):
                continue
            print(zip_info.filename)
            my_zip_open = zipfile.ZipFile("/tmp/dl.zip")
            df = pd.read_csv(zipfile.Path(my_zip_open, zip_info.filename).open())
            print(df.describe())


def describe_all_csvs_in_zips(fs):
    for zip_name in get_zips(fs):
        print(zip_name)
        my_zip = ZipFileSystem("/tmp/dl.zip")
        for fname in my_zip.find(""):
            if not fname.endswith(".csv"):
                continue
            print(fname)
            df = pd.read_csv(my_zip.open(fname))
            print(df.describe())


describe_all_csvs_in_zips(fs)
dlf = fsspec.open("/tmp/dl.zip")
with dlf as f:
    zipf = zipfile.ZipFile(f)
    print(zipf.infolist())
dlf.close()

d1f = fsspec.open("zip://dummy1.csv::/tmp/dl.zip", "rt")
with d1f as f:
    print(f.read())

#d1f = fsspec.open("zip://dummy1.csv::github://tiagoantao:python-performance@/08-persistence/sec1-fsspec/dummy.zip")

#with d1f as f:
#    print(pd.read_csv(f))


zfs = ZipFileSystem("/tmp/dl.zip")
arrow_fs = PyFileSystem(FSSpecHandler(zfs))
my_csv = csv.read_csv(arrow_fs.open_input_stream("dummy1.csv"))
print(my_csv)
#with fsspec.open("zip:local.zip/dummy1.csv") as f:
#    pd.read_csv(f)

##fsa = fsspec.get_mapper("github://tiagoantao:python-performance@")
##print(fsa)
## fs = fsspec.open("git_https.py")
## with fs as f:
##     print(f)
