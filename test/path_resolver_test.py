import unittest
from lib.graphical import GraphicalTSP
from lib.graph_resolver import GraphResolver
from lib.tsp import TSP


class TSPTests(unittest.TestCase):
    def setUp(self):
        nodes = "Gdansk ( 18.60 54.20 )\nBydgoszcz ( 17.90 53.10 )\nKolobrzeg ( 16.10 54.20 )\nKatowice ( 18.80 50.30 )"
        links = "Link_0_10 ( Gdansk Bydgoszcz ) \nLink_0_2 ( Gdansk Kolobrzeg )\nLink_1_2 ( Bydgoszcz Kolobrzeg )\nLink_1_3 ( Katowice Kolobrzeg )\nLink_1_4 ( Bydgoszcz Katowice )"
        self.graphical = GraphicalTSP(nodes, links)
        self.dist_map = TSP(self.graphical)._dist_map

    def test_paths(self):
        path_map = GraphResolver.build_path_map(self.graphical, self.dist_map)

        self.assertListEqual(path_map[0, 1], [[1, 0], [1, 2, 0], [1, 3, 2, 0]])
        self.assertListEqual(path_map[0, 3], [[3, 1, 0], [3, 1, 2, 0], [3, 2, 0], [3, 2, 1, 0]])
        self.assertListEqual(path_map[1, 2],[[2, 0, 1], [2, 1], [2, 3, 1]])


if __name__ == '__main__':
    unittest.main()
