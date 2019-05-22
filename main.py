from models.models import Transponder, Band, Demand
from lib.graphical import Graphical
from lib.tsp import TSP
from lib.read_demands import read_demands
import xml.etree.ElementTree as ET
import numpy as np


tree = ET.parse('data/polska.xml')
data_xml_root = tree.getroot()

transponders = [
    Transponder(id=1, bitrate=40, power_budget=10,
                cost=3, frequency_width=2),
    Transponder(id=2, bitrate=100, power_budget=15.85,
                cost=5, frequency_width=3),
    Transponder(id=3, bitrate=200, power_budget=31.62,
                cost=7, frequency_width=4),
    Transponder(id=4, bitrate=400, power_budget=158.49,
                cost=9, frequency_width=6),
]

bands = [
    Band(id=1, cost=1, frequency_range_from=1,
         frequency_range_to=384, loss_per_km=0.046),
    Band(id=2, cost=2, frequency_range_from=385,
         frequency_range_to=768, loss_per_km=0.055),
]

demands = read_demands(data_xml_root)

tsp = TSP(Graphical(data_xml_root))

print(tsp.path_length(demands[0].paths[0]))