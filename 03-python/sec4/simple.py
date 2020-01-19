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
            calls.append(''.join(toks[4:]))
    return calls


calls = get_chrom(1)

print(len(calls[0]))
print(sys.getsizeof(calls[0]))
print(sys.getsizeof(calls[0][0]))
