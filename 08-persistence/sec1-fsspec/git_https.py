import fsspec
from fsspec.implementations.github import GithubFileSystem

fs = GithubFileSystem("tiagoantao", "python-performance")
print(fs.ls(""))
print(fs.ls("07-pandas/sec2-speed"))
#fsa = fsspec.get_mapper("github://tiagoantao:python-performance@")
#print(fsa)
# fs = fsspec.open("git_https.py")
# with fs as f:
#     print(f)


# https://arrow.apache.org/docs/python/filesystems.html#using-fsspec-compatible-filesystems
