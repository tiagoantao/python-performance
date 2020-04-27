from collections import defaultdict
import multiprocessing as mp
from time import sleep


def report_progress(map_return, tag, callback):
    not_done = 1
    done = 0
    while not_done > 0:
        not_done = 0
        done = 0
        for fut in futures:
            if fut.done():
                done +=1
            else:
                not_done += 1
        sleep(0.5)
        if callback:
            callback(tag, done, not_done)
    

def map_reduce(my_input, mapper, reducer, callback=None):
    with mp.Pool(2) as pool:
        map_results = pool.map(mapper, my_input)
        distributor = defaultdict(list)
        for key, value in map_results:
            distributor[key].append(value)
        results = pool.map(reducer, distributor.items())
    return results


def emitter(word):
    sleep(1)
    return word, 1


def counter(emitted):
    return emitted[0], sum(emitted[1])


def reporter(tag, done, not_done):
    print(f'Operation {tag}: {done}/{not_done}')


words = 'Python is great Python rocks'.split(' ')
a = map_reduce(words, emitter, counter, reporter)

for i in sorted(a, key=lambda x: x[1]):
    print(i)
