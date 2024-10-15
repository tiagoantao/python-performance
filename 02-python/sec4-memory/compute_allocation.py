from array import array
from collections.abc import Iterable, Mapping
from sys import getsizeof
from types import GeneratorType


def compute_allocation(obj) -> tuple[int, int]:
    my_ids = set([id(obj)])
    to_compute = [obj]
    allocation_size = 0
    container_allocation = 0
    while len(to_compute) > 0:
        obj_to_check = to_compute.pop()
        allocation_size += getsizeof(obj_to_check)
        if type(obj_to_check) == str:
            continue
        if type(obj_to_check) == array:
            continue
        elif isinstance(obj_to_check, GeneratorType):
            continue
        elif isinstance(obj_to_check, Mapping):
            container_allocation += getsizeof(obj_to_check)
            for ikey, ivalue in obj_to_check.items():
                if id(ikey) not in my_ids:
                    my_ids.add(id(ikey))
                    to_compute.append(ikey)
                if id(ivalue) not in my_ids:
                    my_ids.add(id(ivalue))
                    to_compute.append(ivalue)
        elif isinstance(obj_to_check, Iterable):
            container_allocation += getsizeof(obj_to_check)
            for inner in obj_to_check:
                if id(inner) not in my_ids:
                    my_ids.add(id(inner))
                    to_compute.append(inner)
    return allocation_size, allocation_size - container_allocation
