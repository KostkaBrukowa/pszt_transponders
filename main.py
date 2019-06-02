import xml.etree.ElementTree as ET
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

# genotype_1 = problem.new_genotype()

# genotype_1 = problem.new_genotype()

# combined_genotype = genotype_1.crossover(genotype_1)


# print("genotype_1 = ", genotype_1.data)
# print("genotype_1 = ", genotype_1.data)
# print("combined_genotype = ", combined_genotype.data)

# mutated_genotype_1 = genotype_1.mutation()

# print("mutated_genotype_1 = ", mutated_genotype_1.data)

# print(genotype_1 == mutated_genotype_1)

gen_alg = GeneticAlgorithm(problem, 200, 1000, 0.05)

gen_alg.init_population()


while True:
     gen_alg.generate_new_population()
     # y = [x.data for x in gen_alg.P]
     # print(y)
     print(gen_alg.P[0].get_cost())
     print(gen_alg.P[0].data)

