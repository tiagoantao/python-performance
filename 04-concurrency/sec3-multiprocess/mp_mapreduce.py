from collections import defaultdict
import multiprocessing as mp
from time import sleep


def report_progress(map_returns, tag, callback):
    done = 0
    num_jobs = len(map_returns)
    while num_jobs > done:
        done = 0
        for ret in map_returns:
            if ret.ready():
                done += 1
        sleep(0.5)
        if callback:
            callback(tag, done, num_jobs - done)


def async_map(pool, mapper, data):
    async_returns = []
    for datum in data:
        async_returns.append(pool.apply_async(
            mapper, (datum, )))  #The tuple
    return async_returns


def map_reduce(pool, my_input, mapper, reducer, callback=None):
    map_returns = async_map(pool, mapper, my_input)
    report_progress(map_returns, 'map', callback)
    map_results = [ret.get() for ret in map_returns]
    distributor = defaultdict(list)
    for key, value in map_results:
        distributor[key].append(value)
    returns = async_map(pool, reducer, distributor.items())
    results = [ret.get() for ret in returns]
    return results


def emitter(word):
    sleep(1)
    return word, 1


def counter(emitted):
    return emitted[0], sum(emitted[1])


def reporter(tag, done, not_done):
    print(f'Operation {tag}: {done}/{done+not_done}')


words = 'Python is great Python rocks'.split(' ')
pool = mp.Pool(2)
results = map_reduce(pool, words, emitter, counter, reporter)
pool.close()
pool.join()


for result in sorted(results, key=lambda x: x[1]):
    print(result)
