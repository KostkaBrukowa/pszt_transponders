from dataclasses import dataclass
from typing import Set, List, Tuple


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


'''
This class represents one specific result for one specific
demand. Also has methods to check if the result is correct
i.e. that the power budget is not exceeded or demand is fulfilled
'''
@dataclass
class Result():
    id: int
    demand: Demand
    path: int
    # list of tuples (frequency, transponder)
    transponders: List[Tuple[int, Transponder]]

    def power_budget_exceeded(self, bands: List[Band]):
        path_length = self.demand.paths[self.path][0]
        return any([
            path_length * band.loss_per_km > transponder.power_budget
            for frequency, transponder in self.transponders
            for band in bands
            if band.contains_frequency(frequency)
        ])

    def demand_not_fulfilled(self):
        return (sum([
            transponder.bitrate for _, transponder in self.transponders
        ]) < self.demand.bitrate)

    def is_correct(self, bands: List[Band]) -> bool:
        return not (self.power_budget_exceeded(bands)
                    or self.demand_not_fulfilled())

    def cost(self) -> float:
        return sum([transponder.cost for _, transponder in self.transponders])
