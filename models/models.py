from dataclasses import dataclass
from typing import Set, List


@dataclass(frozen=True)
class FrequencySlice():
    id: int
    range_from: float
    range_to: float

    def __hash__(self):
        return hash(self.id)


@dataclass(frozen=True)
class Transponder():
    id: int
    bitrate: float
    power_budget: float
    cost: float
    frequency_slices: Set[FrequencySlice]


@dataclass(frozen=True)
class Band():
    id: int
    cost: float
    frequency_slices: Set[FrequencySlice]


@dataclass(frozen=True)
class Demand():
    id: int
    node1: int
    node2: int
    bitrate: float
