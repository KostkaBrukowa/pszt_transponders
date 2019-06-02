from dataclasses import dataclass
from typing import Set, List, Tuple
from .graph import Graph
# from .calculate_result import calculate_result
from .pick_transponders import pick_transponders
import numpy as np
from itertools import combinations

from random import randrange, random


@dataclass(frozen=True)
class Transponder():
    id: int
    bitrate: float
    power_budget: float
    cost: float
    frequency_width: int


@dataclass(frozen=True)
class Band():
    id: int
    cost: float
    frequency_range_from: int
    frequency_range_to: int
    loss_per_km: float

    def contains_frequency(self, frequency: int):
        return (frequency >= self.frequency_range_from and
                frequency <= self.frequency_range_to)


@dataclass(frozen=True)
class Demand():
    id: int
    node1: int
    node2: int
    bitrate: float
    # list of tuples (path length, path)
    paths: List[Tuple[float, List[int]]]


@dataclass
class DemandResult():
    transponders: List[Tuple[int, Transponder]]
    demand: Demand


@dataclass
class Problem():
    graph: Graph
    demands: List[Demand]

    def new_genotype(self):
        data = []

        for demand in self.demands:
            upper_range = len(demand.paths)
            data.append(randrange(upper_range))

        return Genotype(data, self)


@dataclass
class Genotype():
    data: List[int]
    problem: Problem


    # multi-point crossing
    def crossing(self, other_genom):

        center = len(self.data) // 2
        point_1 = randrange(0, center)
        point_2 = randrange(center, len(self.data))

        new_data = (self.data[0: point_1]
                    + other_genom.data[point_1: point_2]
                    + self.data[point_2: len(self.data)])

        return Genotype(new_data, self.problem)

    def mutation(self):
        random_int = randrange(0, len(self.data))

        upper_range = len(self.problem.demands[random_int].paths)
        new_data = self.data[:]
        new_data[random_int] = randrange(upper_range)

        return Genotype(new_data, self.problem)

    def _update_band_map(self, band_map, frequency_needed, path):
        for start, end in zip(path, path[1:]):
            band_map[start, end] += frequency_needed
            band_map[end, start] += frequency_needed

    def _pick_frequencies_for_transponders(self, min_frequency, transponders):
        current_frequency = min_frequency
        transponders_with_frequencies = []
        for transponder in transponders:
            transponders_with_frequencies.append(
                (current_frequency, transponder))
            current_frequency += transponder.frequency_width

        return transponders_with_frequencies

    def _pick_band_cost(self, frequency, bands):
        if frequency == 1:
            return 0

        if bands[-1].frequency_range_to < frequency:
            return float('inf')

        bands_sum = 0
        for band in bands:
            if band.frequency_range_from > frequency:
                break

            bands_sum += band.cost

        return bands_sum

    def calculate_result(self, bands: List[Band], transponders: List[Transponder]):
        """
        calculate result based on data. returns 
        tuple of [cost of whole result, band_map, demands with frequencies]
        cost -> float
        band_map -> 2D nd_array with values as lowest free frequency on an edge
        demands with frequencies -> List[DemandResult]
        """
        demands_result = []
        graph = self.problem.graph
        band_map = np.ones([graph.dimension, graph.dimension], dtype=int)

        for index, demand in enumerate(self.problem.demands):
            path_length, path = demand.paths[self.data[index]]
            picked_transponders = pick_transponders(
                demand.bitrate, path_length, transponders, bands[-1])

            frequency_width_needed = sum(
                [t.frequency_width for t in picked_transponders])

            min_frequency = max([band_map[start, end]
                                 for start, end in zip(path, path[1:])])

            transponders_with_frequencies = self._pick_frequencies_for_transponders(
                min_frequency, picked_transponders)

            self._update_band_map(band_map, frequency_width_needed, path)

            demands_result.append(DemandResult(
                transponders_with_frequencies, demand))

        transponders_cost = sum([transponder.cost for demand_result in demands_result
                                 for _, transponder in demand_result.transponders])

        bands_cost = sum([self._pick_band_cost(band_map[start, end], bands)
                          for start, end in combinations(range(self.problem.graph.dimension), 2)])

        return transponders_cost + bands_cost, band_map, demands_result


@dataclass        
class GeneticAlgorithm():
    P: List[Genotype]
    len_of_P: int

    R: List[Genotype]
    len_of_R: int

    problem: Problem

    probability_of_mutation: float

    def __init__(self, problem, len_of_P, len_of_R, probability_of_mutation ):
        self.problem = problem
        self.len_of_P = len_of_P
        self.len_of_R = len_of_R
        self.probability_of_mutation = probability_of_mutation
        self.P = []
        self.R = []

    def init_population(self):
        self.P.clear()
        for i in range(self.len_of_P):
            self.P.append(self.problem.new_genotype())

    def generate_new_population(self):
        self.R.clear()
        for i in range(self.len_of_R):
            number_of_genotype_1 = randrange(self.len_of_P)
            number_of_genotype_2 = randrange(self.len_of_P)
            new_genotype = self.P[number_of_genotype_1].crossover(self.P[number_of_genotype_2])
            self.R.append(new_genotype)

        for i in range(self.len_of_R):
            if random() <= self.probability_of_mutation:
                self.R[i] = self.R[i].mutation()
        
        P_union_R = self.P + self.R
        P_union_R.sort(key=lambda x: x.get_cost())

        self.P = P_union_R[0:self.len_of_P]
