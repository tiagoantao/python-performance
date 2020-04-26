from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor as Executor
from time import sleep


def map_reduce_less_naive(my_input, mapper, reducer, callback=None):
    with Executor(max_workers=2) as executor:
        futures = async_map(executor, mapper, my_input)
        report_progress(futures, 'map', callback)
        #wait(futures).done
        map_results = map(lambda f: f.result(), futures)
        distributor = defaultdict(list)
        for key, value in map_results:
            distributor[key].append(value)

        futures = async_map(executor, reducer, distributor.items())
        report_progress(futures, 'reduce', callback)
        #wait(futures).done
        results = map(lambda f: f.result(), futures)
    return results


def emitter(word):
    #sleep(10)
    return word, 1


counter = lambda emitted: (emitted[0], sum(emitted[1]))

def reporter(tag, done, not_done):
    print(f'Operation {tag}: {done}/{done+not_done}')

words = 'Python is great Python rocks'.split(' ')
a = map_reduce_less_naive(words, emitter, counter, reporter)

for i in sorted(a, key=lambda x: x[1]):
    print(i)
