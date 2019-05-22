from dataclasses import dataclass
from typing import Set, List


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
    paths: List[List[int]]
