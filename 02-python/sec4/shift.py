import sys
from timeit import timeit
from typing import List, Tuple


sys.path.insert(0, '../shared')

ENCODE_SNPS = 14


def encode_snps(snps: List[str]) -> Tuple[Tuple[str], List[int]]:
    allele_pos = tuple(set(snps))
    enc_list = []
    for i in range(len(snps) // ENCODE_SNPS):
        enc = 0
        for j in range(ENCODE_SNPS):
            if j > 0:
                enc <<= 2
            enc += allele_pos.index(snps[i * ENCODE_SNPS + j])
        enc_list.append(enc)
    return allele_pos, enc_list


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
            calls.append(encode_snps(toks[4:])[1])
    return calls


calls = get_chrom(1)

print(len(calls[0]))
print(sys.getsizeof(calls[0]))
print(sys.getsizeof(calls[0][0]))
