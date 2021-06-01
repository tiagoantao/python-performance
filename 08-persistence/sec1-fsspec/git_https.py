import fsspec
from fsspec.implementations.github import GithubFileSystem

fs = GithubFileSystem("tiagoantao", "python-performance")
print(fs.ls(""))
print(fs.ls("08-persistence/sec1-fsspec"))
for root, dirs, files in fs.walk(""):
    print(root)
#fsa = fsspec.get_mapper("github://tiagoantao:python-performance@")
#print(fsa)
# fs = fsspec.open("git_https.py")
# with fs as f:
#     print(f)


# https://arrow.apache.org/docs/python/filesystems.html#using-fsspec-compatible-filesystems
