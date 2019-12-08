from collections import defaultdict
from functools import reduce
import os
from typing import Dict, List, Tuple

from zarr.hierarchy import Array

PLINK_PREF = 'my_hapmap'
ZARR_DB = 'db.zarr'
NUM_WORKERS = os.cpu_count()  # Is this cores, processors or threads?
NUM_SAMPLES = 210



def get_population_map(pop_file: str) -> Dict[str, Dict[str, str]]:
    # Not using the family component of the individual
    pop_map = defaultdict(list)
    individual_map = {}
    with open(pop_file) as f:
        for line in f:
            tokens = line.rstrip().split(' ')
            individual = tokens[1]
            population = tokens[2]
            pop_map[population].append(individual)
            individual_map[individual] = population
    return {'population_map': pop_map,
            'individual_map': individual_map}


def call_positions_for_pop(
        pop_map: Dict[str, str],
        sample_order: List[str]) -> Dict[str, List[int]]:
    pos_for_pops = {}
    for pop, indivs in pop_map.items():
        pos_for_pops[pop] = map(sample_order.find, indivs)
    return pos_for_pops


def split_samples_per_pop(
        individual_map: Dict[str, str],
        sample_order: Array,
        chrom_calls: Array) -> Dict[str, Array]:
    pops = set(individual_map.keys())
    for variant in range(chrom_calls.shape[0]):
        samples_per_pop = {}
        for pop in pops:
            samples_per_pop[pop] = map(
                lambda x: x[1],
                filter(
                    lambda x: x[0] == pop,
                    zip(
                        sample_order,
                        chrom_calls[variant, :])))
        yield samples_per_pop


def get_maf(calls: Array) -> Tuple:
    counts = reduce(
        lambda x, y: (x[0] + y[0], x[1] + y[1]),
        map(lambda x: (2 - x, x), calls),
        # The encoding is 0 - ho for 1st allele, 1 hz, 2 - ho for second (and 3 for NA)
        # Hence the formula above
        (0, 0))
    all_sum = sum(counts)
    return min(counts[0] / all_sum, counts[1] / all_sum)
