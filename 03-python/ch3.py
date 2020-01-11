import sys

import numpy as np
from zarr import Group

sys.path.insert(0, '../shared')

from utilities import NUM_SAMPLES  # noqa: E402


def encode_alleles(a1: str, a2: str, code: str) -> int:
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
def conv_chrom(fname: str, block_size: int,
               root: Group, chrom: int) -> None:
    num_positions = 0
    with open(fname) as tfam:
        for line in tfam:  # redo this with generators
            tokens = line.rstrip().split(' ')
            l_chrom = int(tokens[0])
            if l_chrom < chrom:
                continue
            elif l_chrom > chrom:
                break
            num_positions += 1
    tfam = open(fname)
    chrom_group = root.create_group(f'chromosome-{chrom}')
    all_calls = chrom_group.zeros('calls', shape=(num_positions, NUM_SAMPLES),
                                  dtype='B')
    block = []
    all_positions = []
    all_alleles = []
    current_position = 0
    for line in tfam:  # redo this with generators
        tokens = line.rstrip().split(' ')
        l_chrom = int(tokens[0])
        if l_chrom < chrom:
            continue
        elif l_chrom > chrom:
            break
        position = int(tokens[3])
        all_positions.append(position)
        calls = tokens[4:]
        alleles = ''.join(set(calls[4:]) - set(['0']))
        if len(alleles) == 1:
            alleles += alleles
        all_alleles.append(alleles)
        sample_calls = np.empty(shape=NUM_SAMPLES, dtype='B')
        for sample_position, sample in enumerate(range(NUM_SAMPLES)):
            a1, a2 = calls[2 * sample: 2 * sample + 2]
            try:
                sample_calls[sample_position] = encode_alleles(a1, a2, alleles)
            except Exception:
                print(chrom, current_position, sample_position)
                raise
        block.append(sample_calls)
        current_position += 1
        if current_position % block_size == 0:
            all_calls[current_position - block_size:current_position, :] = block
            block = []
    if len(block) > 0:
        all_calls[- len(block):, :] = block
    chrom_group.array('positions', all_positions)
    chrom_group.array('alleles', all_alleles)
