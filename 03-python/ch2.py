from functools import lru_cache
import sys
sys.path.insert(0, '../shared')
from typing import Callable, List, IO, Set

import numpy as np
from zarr import Group

from utilities import NUM_SAMPLES


def encode_alleles(a1: str, a2: str, code: List[str]) -> int:
    if a1 == '0' or a2 == '0':
        return 3
    if a1 == a2:
        return 1
    if a1 == code[0]:
        return 0
    return 2


@lru_cache(None)  # XXX This will not be required with 3.8
def encode_alleles_tuple(a1: str, a2: str, code: Set[str]) -> int:
    if a1 == '0' or a2 == '0':
        return 3
    if a1 == a2:
        return 1
    if a1 == code[0]:
        return 0
    return 2


if 'profile' not in __builtins__:
    def profile(f):
        def wrapper(*args, **kwargs):
            f(*args, **kwargs)
        return wrapper


@profile
def conv_chrom(fname: str, block_size: int, max_positions: int,
               root: Group, chrom: int,
               encode_alleles: Callable = encode_alleles,
               encode_fun: Callable = list) -> None:
    tfam = open(fname)
    chrom_group = root.create_group(f'chromosome-{chrom}')

    all_calls = chrom_group.zeros('calls', shape=(max_positions, NUM_SAMPLES), dtype='B')
    block = []
    current_position = 0
    for count, line in enumerate(tfam):
        tokens = line.rstrip().split(' ')
        calls = tokens[4:]
        alleles = encode_fun(set(calls[4:]) - set([0]))
        sample_calls = np.empty(shape=NUM_SAMPLES, dtype='B')
        for sample_position, sample in enumerate(range(NUM_SAMPLES)):
            a1, a2 = calls[2 * sample: 2 * sample + 2]
            try:
                sample_calls[sample_position] = encode_alleles(a1, a2, alleles)
            except:
                print(chrom, count, sample_position, num_samples, len(positions))
                raise
        block.append(sample_calls)
        if count % block_size == block_size - 1:
            all_calls[current_position:current_position+block_size, :] = block
            block = []
        if count % max_positions == max_positions - 1:
            break
