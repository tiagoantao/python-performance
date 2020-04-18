from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor as Executor


def map_reduce_still_naive(my_input, mapper, reducer):
    map_results = map(mapper, my_input)

    distributor = defaultdict(list)
    for key, value in map_results:
        distributor[key].append(value)

    with Executor(max_workers=1) as executor:
        results = executor.map(reducer, distributor.items())
    print(results)
    return results


words = filter(lambda x: x!= '', map(lambda x: x.strip().rstrip(), ' '.join(open('text.txt', 'rt', encoding='utf-8').readlines()).split(' ')))

emiter = lambda word: (word, 1)
def counter(emitted):
    return emitted[0], sum(emitted[1])

a = list(map_reduce_still_naive(words, emiter, counter))

for i in sorted(a, key=lambda x: x[1]):
    print(i)
