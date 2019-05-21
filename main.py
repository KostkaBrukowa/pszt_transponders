from models.models import FrequencySlice, Transponder, Band, Demand
from lib.graphical import GraphicalTSP
from lib.tsp import TSP
import numpy as np

frequency_slices = [FrequencySlice(id=1, range_from=10, range_to=20),
                    FrequencySlice(2, 20, 30),
                    FrequencySlice(3, 30, 40)]

transponders = [
    Transponder(id=1, bitrate=10, power_budget=10,
                cost=200, frequency_slices=set([frequency_slices[1]])),
    Transponder(id=2, bitrate=20, power_budget=15,
                cost=200, frequency_slices=set(frequency_slices)),
    Transponder(id=3, bitrate=30, power_budget=30,
                cost=200, frequency_slices=set([frequency_slices[2]])),
]

bands = [
    Band(id=1, cost=3000, frequency_slices=set(frequency_slices[:2])),
    Band(id=2, cost=2000, frequency_slices=set([frequency_slices[1]])),
    Band(id=3, cost=3000, frequency_slices=set(frequency_slices[1:])),
]

demands = [
    Demand(id=1, node1=1, node2=2, bitrate=20),
    Demand(id=2, node1=1, node2=3, bitrate=10),
    Demand(id=3, node1=2, node2=3, bitrate=15),
]


# nodes = "Gdansk ( 18.60 54.20 )\nBydgoszcz ( 17.90 53.10 )\nKolobrzeg ( 16.10 54.20 )\nKatowice ( 18.80 50.30 )"
# links = "Link_0_10 ( Gdansk Bydgoszcz ) \nLink_0_2 ( Gdansk Kolobrzeg )\nLink_1_2 ( Bydgoszcz Kolobrzeg )\nLink_1_3 ( Katowice Kolobrzeg )\nLink_1_4 ( Bydgoszcz Katowice )"

nodes = "Gdansk ( 18.60 54.20 )\nBydgoszcz ( 17.90 53.10 )\nKolobrzeg ( 16.10 54.20 )\nKatowice ( 18.80 50.30 )\nKrakow ( 19.80 50.00 )\nBialystok ( 23.10 53.10 )\nLodz ( 19.40 51.70 )\nPoznan ( 16.80 52.40 )\nRzeszow ( 21.90 50.00 )\nSzczecin ( 14.50 53.40 )\nWarsaw ( 21.00 52.20 )\nWroclaw ( 16.90 51.10 )"
links = "Link_0_10 ( Gdansk Warsaw ) 0.00 0.00 0.00 156.00 ( 155.00 156.00 622.00 468.00 )\nLink_0_2 ( Gdansk Kolobrzeg ) 0.00 0.00 0.00 272.00 ( 155.00 272.00 622.00 816.00 )\nLink_1_2 ( Bydgoszcz Kolobrzeg ) 0.00 0.00 0.00 156.00 ( 155.00 156.00 622.00 468.00 )\nLink_1_7 ( Bydgoszcz Poznan ) 0.00 0.00 0.00 186.00 ( 155.00 186.00 622.00 558.00 )\nLink_1_10 ( Bydgoszcz Warsaw ) 0.00 0.00 0.00 272.00 ( 155.00 272.00 622.00 816.00 )\nLink_2_9 ( Kolobrzeg Szczecin ) 0.00 0.00 0.00 237.00 ( 155.00 237.00 622.00 711.00 )\nLink_3_4 ( Katowice Krakow ) 0.00 0.00 0.00 208.00 ( 155.00 208.00 622.00 624.00 )\nLink_3_6 ( Katowice Lodz ) 0.00 0.00 0.00 181.00 ( 155.00 181.00 622.00 543.00 )\nLink_3_11 ( Katowice Wroclaw ) 0.00 0.00 0.00 208.00 ( 155.00 208.00 622.00 624.00 )\nLink_4_8 ( Krakow Rzeszow ) 0.00 0.00 0.00 250.00 ( 155.00 250.00 622.00 750.00 )\nLink_4_10 ( Krakow Warsaw ) 0.00 0.00 0.00 324.00 ( 155.00 324.00 622.00 972.00 )\nLink_5_8 ( Bialystok Rzeszow ) 0.00 0.00 0.00 324.00 ( 155.00 324.00 622.00 972.00 )\nLink_5_10 ( Bialystok Warsaw ) 0.00 0.00 0.00 250.00 ( 155.00 250.00 622.00 750.00 )\nLink_6_10 ( Lodz Warsaw ) 0.00 0.00 0.00 165.00 ( 155.00 165.00 622.00 495.00 )\nLink_6_11 ( Lodz Wroclaw ) 0.00 0.00 0.00 305.00 ( 155.00 305.00 622.00 915.00 )\nLink_7_9 ( Poznan Szczecin ) 0.00 0.00 0.00 142.00 ( 155.00 142.00 622.00 426.00 )\nLink_7_11 ( Poznan Wroclaw ) 0.00 0.00 0.00 195.00 ( 155.00 195.00 622.00 585.00 )\nLink_0_5 ( Gdansk Bialystok ) 0.00 0.00 0.00 294.00 ( 155.00 294.00 622.00 882.00 )"


graphical_tsp = GraphicalTSP(nodes, links)
tsp = TSP(graphical_tsp)
print(tsp._path_map[2, 1])  
