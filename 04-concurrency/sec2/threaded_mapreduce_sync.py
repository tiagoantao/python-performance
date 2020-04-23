from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor as Executor


def map_reduce_still_naive(my_input, mapper, reducer):
    with Executor() as executor:
        map_results = executor.map(mapper, my_input)

        distributor = defaultdict(list)
        for key, value in map_results:
            distributor[key].append(value)
        results = executor.map(reducer, distributor.items())
    return results


words = filter(lambda x: x!= '', map(lambda x: x.strip().rstrip(), ' '.join(open('text.txt', 'rt', encoding='utf-8').readlines()).split(' ')))

emiter = lambda word: (word, 1)
counter = lambda emitted: (emitted[0], sum(emitted[1]))

a = list(map_reduce_still_naive(words, emiter, counter))

for i in sorted(a, key=lambda x: x[1]):
    print(i)
