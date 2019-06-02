import unittest
from lib.telecommunication import Transponder, Band, Demand, Problem, Genom
from lib.graphical import Graphical
from itertools import combinations


class MockedGraph():
    def __init__(self, dimension):
        self.dimension = dimension


class TSPTests(unittest.TestCase):
    def setUp(self):
        self.transponders = [
            Transponder(id=1, bitrate=40, power_budget=10,
                        cost=3, frequency_width=2),
            Transponder(id=2, bitrate=100, power_budget=15.85,
                        cost=5, frequency_width=3)
        ]

        self.bands = [
            Band(id=1, cost=1, frequency_range_from=1,
                 frequency_range_to=384, loss_per_km=0.046),
            Band(id=2, cost=2, frequency_range_from=385,
                 frequency_range_to=768, loss_per_km=0.055),
        ]

        self.demands = [
            Demand(id=1, node1=1, node2=2, bitrate=100,
                   paths=[(10, [1, 2]), (14, [1, 3, 2])]),
            Demand(id=2, node1=1, node2=3, bitrate=80,
                   paths=[(10, [1, 3]), (14, [1, 2, 3])]),
        ]

        graph = MockedGraph(4)
        self.problem: Problem = Problem(graph, self.demands)

    def test_genom_cost(self):
        genom = Genom(data=[1, 1], problem=self.problem)

        cost, _, _ = genom.calculate_result(self.bands, self.transponders)

        self.assertEqual(
            cost, 2 * self.transponders[1].cost + 3 * self.bands[0].cost)

    def test_genom_cost_with_two_bands(self):
        bands = [
            Band(id=1, cost=1, frequency_range_from=1,
                 frequency_range_to=4, loss_per_km=0.046),
            Band(id=2, cost=2, frequency_range_from=5,
                 frequency_range_to=20, loss_per_km=0.055),
        ]

        genom = Genom(data=[1, 1], problem=self.problem)

        cost, _, _ = genom.calculate_result(bands, self.transponders)

        self.assertEqual(
            cost, 2 * self.transponders[1].cost + 3 * bands[0].cost + bands[1].cost)

    def test_genom_cost_with_invalid_transponders(self):
        bands = [
            Band(id=1, cost=1, frequency_range_from=1,
                 frequency_range_to=4, loss_per_km=0.046),
        ]

        genom = Genom(data=[1, 1], problem=self.problem)

        cost, _, _ = genom.calculate_result(bands, self.transponders)

        self.assertEqual(cost, float('inf'))

    def test_band_map(self):
        genom = Genom(data=[1, 1], problem=self.problem)

        _, band_map, _ = genom.calculate_result(self.bands, self.transponders)

        '''paths are [1,3,2] and [1,2,3] with second transponder'''
        self.assertEqual(band_map[1, 3], 4)

        self.assertEqual(band_map[1, 2], 4)

        self.assertEqual(band_map[3, 2], 7)

        for i, j in combinations(range(len(band_map)), 2):
            self.assertEqual(band_map[i, j], band_map[j, i])

    def test_transponders_frequency(self):
        genom = Genom(data=[1, 1], problem=self.problem)

        _, _, demands_result = genom.calculate_result(
            self.bands, self.transponders)

        self.assertEqual(demands_result[0].transponders[0][0], 1)
        self.assertEqual(demands_result[1].transponders[0][0], 4)

    def test_transponders_frequency_multiple_tranponders(self):
        demands = [
            Demand(id=1, node1=1, node2=2, bitrate=200,
                   paths=[(10, [1, 2]), (14, [1, 3, 2])]),
        ]

        problem = Problem(MockedGraph(4), demands)

        genom = Genom(data=[1, 1], problem=problem)

        _, _, demands_result = genom.calculate_result(
            self.bands, self.transponders)

        self.assertEqual(demands_result[0].transponders[0][0], 1)
        self.assertEqual(demands_result[0].transponders[1][0], 4)


if __name__ == '__main__':
    unittest.main()
