import sys
from timeit import timeit
from typing import List, Set


sys.path.insert(0, '../shared')


def get_chrom(my_chrom):
    calls = []
    with open('my_hapmap.tped') as f:
        for l in f:
            toks = l.rstrip().split(' ')
            chrom = int(toks[0])
            if chrom < my_chrom:
                continue
            if chrom > my_chrom:
                break
            calls.append(toks[4:])
    return calls


calls = get_chrom(1)

size_calls = len(calls)

size_list = sys.getsizeof(calls)
print(f'Number of SNPs on chromsome 1: {size_calls}')
print(f'Memory size of the list: {size_list}')
print(f'Memory per SNP {size_list // size_calls}')

print(sys.getsizeof(calls[0]))
print(sys.getsizeof('A'))

all_ids = set()
for SNP in calls:
    for obj in SNP:
        all_ids.add(id(obj))
print(len(all_ids))
