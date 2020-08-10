import bisect
from random import shuffle
import sys
from timeit import timeit

import zarr

sys.path.insert(0, '../shared')


def in_unordered(my_list, item):
    item in my_list


def in_ordered(my_list, item):
    pos = bisect.bisect_left(my_list, item)
    return pos != len(my_list) and my_list[pos] == item


def in_set(my_set: Set, item: object) -> bool:
    item in my_set


root = zarr.open('db.zarr', mode='r')
positions = root['/chromosome-1/positions']
positions_set = set(positions)

min_position = min(positions)
max_position = max(positions)
middle_location = (max_position + min_position) // 2

print(timeit('in_unordered(positions, middle_location)', number=10,
             globals=locals()) / 10)
print(timeit('in_ordered(positions, middle_location)', number=1000,
             globals=locals()) / 1000)
print(timeit('in_set(positions_set, middle_location)', number=10000,
             globals=locals()) / 10000)


def create_ordered_list(unordered_list: List) -> List:
    my_list = []
    for elem in unordered_list:
        bisect.insort(my_list, elem)


def create_list(unordered_list: List) -> List:
    my_list = []
    for elem in unordered_list:
        my_list.append(elem)


shuffle_positions = list(positions)
shuffle(shuffle_positions)

print(timeit('create_ordered_list(positions)', number=10, globals=locals()) / 10)
print(timeit('create_list(positions)', number=100, globals=locals()) / 100)


print(timeit('create_ordered_list(positions + positions)', number=1, globals=locals()) / 1)
print(timeit('create_list(positions + positions)', number=100, globals=locals()) / 100)
