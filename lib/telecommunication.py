from dataclasses import dataclass
from typing import Set, List, Tuple
from .graph import Graph

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

    cost = None
    solution = None

    #multi-point crossing
    def crossover(self, other_Genotype):
        center = len(self.data) // 2
        point_1 = randrange(0, center)
        point_2 = randrange(center, len(self.data))

        new_data = (self.data[0 : point_1] 
                + other_Genotype.data[point_1 : point_2] 
                + self.data[point_2 : len(self.data)] )

        return Genotype(new_data, self.problem)

    def mutation(self):
        random_int = randrange(0, len(self.data))

        upper_range = len(self.problem.demands[random_int].paths)
        new_data = self.data[:]
        new_data[random_int] = randrange(upper_range)

        return Genotype(new_data, self.problem)

    def get_cost(self):
        if self.cost == None:
            self.calculate_solution()
        return self.cost

    def get_solution(self):
        if self.solution == None:
            self.calculate_solution()
        return self.solution

    def calculate_solution(self):
        # to trzeba napisać
        self.cost = randrange(1,1000000000)
        self.solution = [1,2,3]


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

    
# '''
# This class represents one specific result for one specific
# demand. Also has methods to check if the result is correct
# i.e. that the power budget is not exceeded or demand is fulfilled
# '''
# @dataclass
# class Result():
#     id: int
#     demand: Demand
#     path: int
#     # list of tuples (frequency, transponder)
#     transponders: List[Tuple[int, Transponder]]

#     def power_budget_exceeded(self, bands: List[Band]):
#         path_length = self.demand.paths[self.path][0]
#         return any([
#             path_length * band.loss_per_km > transponder.power_budget
#             for frequency, transponder in self.transponders
#             for band in bands
#             if band.contains_frequency(frequency)
#         ])

#     def demand_not_fulfilled(self):
#         return (sum([
#             transponder.bitrate for _, transponder in self.transponders
#         ]) < self.demand.bitrate)

#     def is_correct(self, bands: List[Band]) -> bool:
#         return not (self.power_budget_exceeded(bands)
#                     or self.demand_not_fulfilled())

#     def cost(self) -> float:
#         return sum([transponder.cost for _, transponder in self.transponders])
