from collections import defaultdict
import sys
from typing import List, Tuple

sys.path.insert(0, '../shared')

def get_chrom(my_chrom: int):
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

def get_chrom_g(my_chrom: int):
    calls = []
    with open('my_hapmap.tped') as f:
        for l in f:
            toks = l.rstrip().split(' ')
            chrom = int(toks[0])
            if chrom < my_chrom:
                continue
            if chrom > my_chrom:
                break
            yield toks[4:]


calls_g = get_chrom_g(1)

print(sys.getsizeof(calls), type(calls))
print(sys.getsizeof(calls_g), type(calls_g))

print(set(next(calls_g)))
# calls_g = get_chrom(1)
num_calls = 0
for call in calls_g:
    num_calls += 1
    
print(num_calls)

def get_chrom_pos(my_chrom: int):
    calls = []
    with open('my_hapmap.tped') as f:
        for l in f:
            toks = l.rstrip().split(' ')
            chrom = int(toks[0])
            if chrom < my_chrom:
                continue
            if chrom > my_chrom:
                break
            yield int(toks[3])
    return calls


positions = list(get_chrom_pos(1))
print(positions[0], positions[-1])
print(positions[-1] // 50000)


def get_maf(calls):
    alleles = set(calls)
    if len(alleles) == 1 or (len(alleles) == 2 and '0' in alleles):
        return None
    counts = defaultdict(int)
    num_calls = 0
    for call in calls:
        if call == '0':
            continue
        counts[call] += 1
        num_calls += 1
    return min([count / num_calls for count in counts.values()])
        
    
