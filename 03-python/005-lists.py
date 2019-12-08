import random
from timeit import timeit

MAX_SIZE = 1000000

big_list = list(range(MAX_SIZE))
big_range = range(MAX_SIZE)
big_set = set(range(MAX_SIZE))

def search_cases(n, where):
    for _ in range(n):
        random.randint(0, 10*MAX_SIZE) in where

print(timeit('search_cases(1000,big_set)', number=5, globals=globals()))
print(timeit('search_cases(1000,big_range)', number=5, globals=globals()))
print(timeit('search_cases(1000,big_list)', number=5, globals=globals()))
