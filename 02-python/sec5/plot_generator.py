from collections import defaultdict
import sys
from typing import List, Tuple

import matplotlib.pyplot as plt

sys.path.insert(0, '../shared')

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

    
chr1_mafs = map(get_maf, get_chrom_g(1))
maf_pos = zip(get_chrom_pos(1), chr1_mafs)

def do_window(size, iterator):
    current_window = 0
    current_content = []
    for pos, content in iterator:
        my_window = pos // size
        if my_window != current_window:
            yield current_content
            while current_window < my_window:
                current_window += 1
                yield []
            current_content = []
        else:
            current_content.append(content)
    if len(current_content) > 0:
        yield current_content


windowed_mafs = do_window(500000, maf_pos)
clean_windows = (
    filter(lambda maf: maf is not None, mafs)
    for mafs in windowed_mafs)


def mean_empty_0(my_list):
    return None if len(my_list) == 0 else sum(my_list) / len(my_list)

def mean_empty(my_iterator):
    my_sum = 0
    cnt = 0
    for e in my_iterator:
        my_sum += e
        cnt += 1
    return None if cnt == 0 else my_sum / cnt


my_means = list(map(mean_empty, clean_windows)) 
plt.plot(my_means, '.')
plt.show()
