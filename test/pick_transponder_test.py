import unittest
from lib.telecommunication import Transponder, Band, Demand
from lib.pick_transponders import pick_transponders
from lib.graphical import Graphical


class TSPTests(unittest.TestCase):
    def setUp(self):
        self.transponders = [
            Transponder(id=1, bitrate=40, power_budget=10,
                        cost=3, frequency_width=2),
            Transponder(id=2, bitrate=100, power_budget=15.85,
                        cost=5, frequency_width=3)
        ]

        self.band = Band(id=2, cost=2, frequency_range_from=385,
                         frequency_range_to=768, loss_per_km=0.055)

    def test_single_transponder(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=100,
                        paths=[(10, [1, 2]), (14, [1, 3, 2])])

        transponders = pick_transponders(
            demand.bitrate, demand.paths[0][0], self.transponders, self.band)

        self.assertCountEqual(transponders, [self.transponders[1]])

    def test_single_transponder1(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=40,
                        paths=[(10, [1, 2]), (14, [1, 3, 2])])

        transponders = pick_transponders(
            demand.bitrate, demand.paths[0][0], self.transponders, self.band)

        self.assertCountEqual(transponders, [self.transponders[0]])

    def test_single_transponder2(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=41,
                        paths=[(10, [1, 2]), (14, [1, 3, 2])])

        transponders = pick_transponders(
            demand.bitrate, demand.paths[0][0], self.transponders, self.band)

        self.assertCountEqual(transponders, [self.transponders[1]])

    def test_multiple_transponders(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=101,
                        paths=[(10, [1, 2]), (14, [1, 3, 2])])

        transponders = pick_transponders(
            demand.bitrate, demand.paths[0][0], self.transponders, self.band)

        self.assertCountEqual(
            transponders, [self.transponders[1], self.transponders[0]])

    def test_multiple_transponders1(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=200,
                        paths=[(10, [1, 2]), (14, [1, 3, 2])])

        transponders = pick_transponders(
            demand.bitrate, demand.paths[0][0], self.transponders, self.band)

        self.assertCountEqual(
            transponders, [self.transponders[1], self.transponders[1]])

    def test_multiple_transponders2(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=201,
                        paths=[(10, [1, 2]), (14, [1, 3, 2])])

        transponders = pick_transponders(
            demand.bitrate, demand.paths[0][0], self.transponders, self.band)

        self.assertCountEqual(transponders, [
            self.transponders[1], self.transponders[1], self.transponders[0]])

    def test_single_transponders_with_power_exceeded(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=201,
                        paths=[(200, [1, 2]), (14, [1, 3, 2])])

        transponders = pick_transponders(
            demand.bitrate, demand.paths[0][0], self.transponders, self.band)

        self.assertCountEqual(transponders, [
            self.transponders[1], self.transponders[1], self.transponders[1]])



if __name__ == '__main__':
    unittest.main()
