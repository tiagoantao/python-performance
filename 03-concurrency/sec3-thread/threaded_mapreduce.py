from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor as Executor
from time import sleep


def report_progress(futures, tag, callback):
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
        if not_done > 0 and callback:
            callback(tag, done, not_done)
    

def async_map(executor, mapper, data):
    futures = []
    for datum in data:
        futures.append(executor.submit(mapper, datum))
    return futures


def map_less_naive(executor, my_input, mapper):
    map_results = async_map(executor, mapper, my_input)
    return map_results


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


words = filter(lambda x: x!= '', map(lambda x: x.strip().rstrip(), ' '.join(open('text.txt', 'rt', encoding='utf-8').readlines()).split(' ')))

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

#words = 'Python is great Python rocks'.split(' ')

#with Executor(max_workers=4) as executor:
#    maps = map_less_naive(executor, words, emitter)
#    print(maps[-1])
#    not_done = 1
#    while not_done > 0:
#        not_done = 0
#        for fut in maps:
#            not_done += 1 if not fut.done() else 0
#        sleep(1)
#        print(f'Still not finalized: {not_done}')
