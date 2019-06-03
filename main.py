import xml.etree.ElementTree as ET
import json
#import numpy as np

from lib.read_demands import read_demands

from lib.telecommunication import Transponder, Band, Demand, Problem
from lib.graphical import Graphical
from lib.graph import Graph

from lib.telecommunication import GeneticAlgorithm

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

graph = Graph(Graphical(data_xml_root))
demands = read_demands(data_xml_root, graph)

problem = Problem(graph, demands, transponders, bands)

gen_alg = GeneticAlgorithm(problem, 2000, 5000, 0.01)
gen_alg.init_population()

period_of_save_result = 10
i = 1
while True:
     gen_alg.generate_new_population()

     print("Epoch nr", i)
     print("Best result:")
     print("   Cost = ", gen_alg.P[0].get_cost())
     print("   Genotype = ", gen_alg.P[0].data)
     print()

     if i % period_of_save_result == 0:
          with open("result/epoch_" + str(i) + ".json", "w") as f:
               best_result = gen_alg.P[0].calculate_result()
               best_result_as_dict = { "cost": best_result[0],
                                   "band_map": best_result[1],
                                   "demands_result": best_result[2]
                                   }
               f.write(str(best_result_as_dict))
     i += 1
     

