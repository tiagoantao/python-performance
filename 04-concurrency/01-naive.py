from collections import defaultdict


def map_reduce_ultra_naive(my_input, mapper, reducer):
    map_results = map(mapper, my_input)

    distributor = defaultdict(list)
    for key, value in map_results:
        distributor[key].append(value)

    return map(reducer, distributor.items())


words = 'Python is great Python rocks'.split(' ')

emiter = lambda word: (word, 1)
counter = lambda emitted: (emitted[0], sum(emitted[1]))


a = list(map_reduce_ultra_naive(words, emiter, counter))

print(a)
