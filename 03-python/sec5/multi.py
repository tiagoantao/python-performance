import array
import sys
from typing import Callable, List, Tuple

sys.path.insert(0, '../shared')
sys.path.insert(0, '.')

from compute_allocation import compute_allocation

ENCODE_SNPS = 16


def encode_snps(snps: List[str]) -> Tuple[Tuple[str], array.array]:
    allele_pos = tuple(set(snps))
    enc_list = []
    for i in range(len(snps) // ENCODE_SNPS):
        enc = 0
        for j in range(ENCODE_SNPS):
            if j > 0:
                enc <<= 2
            enc += allele_pos.index(snps[i * ENCODE_SNPS + j])
        enc_list.append(enc)
    return allele_pos, array.array('I', enc_list)
                                                                                            

def get_chrom(my_chrom: int, fun: Callable) -> List:
    calls = []
    with open('my_hapmap.tped') as f:
        for l in f:
            toks = l.rstrip().split(' ')
            chrom = int(toks[0])
            if chrom < my_chrom:
                continue
            if chrom > my_chrom:
                break
            calls.append(fun(toks[4:]))
    return calls


assert array.array('I', [1]).itemsize == 4
calls_shift = get_chrom(1, lambda x: encode_snps(x)[1])
calls_str = get_chrom(1, lambda x: ''.join(x))
calls = get_chrom(1, lambda x: x)

print(sys.getsizeof(calls_shift), compute_allocation(calls_shift))
print(sys.getsizeof(calls_str), compute_allocation(calls_str))
print(sys.getsizeof(calls), compute_allocation(calls))
