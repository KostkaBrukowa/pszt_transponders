import unittest
from models.models import Transponder, Band, Demand, Result
from lib.graphical import Graphical


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

        # demands = [
        #     Demand(id=1, node1=1, node2=2, bitrate=100,
        #            paths=[(10, [1, 2]), (14, [1, 3, 2])]),
        #     Demand(id=2, node1=1, node2=3, bitrate=80,
        #            paths=[(10, [1, 3]), (14, [1, 2, 3])]),
        # ]

    def test_power_budget_exceeded(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=100,
                        paths=[(1000, [1, 2]), (14, [1, 3, 2])])

        result = Result(1, demand, 0, [(4, self.transponders[0])])

        self.assertTrue(result.power_budget_exceeded(self.bands))
        self.assertFalse(result.is_correct(self.bands))

    def test_power_budget_not_exceeded(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=100,
                        paths=[(100, [1, 2]), (14, [1, 3, 2])])

        result = Result(1, demand, 0, [(4, self.transponders[0])])

        self.assertFalse(result.power_budget_exceeded(self.bands))

    def test_power_demand_not_fulfilled(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=100,
                        paths=[(100, [1, 2]), (14, [1, 3, 2])])

        result = Result(1, demand, 0, [(4, self.transponders[0])])

        self.assertTrue(result.demand_not_fulfilled())
        self.assertFalse(result.is_correct(self.bands))

    def test_power_demand_fulfilled(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=100,
                        paths=[(100, [1, 2]), (14, [1, 3, 2])])

        result1 = Result(1, demand, 0, [(4, self.transponders[0]), (8, self.transponders[0]), (8, self.transponders[0])])
        result2 = Result(1, demand, 0, [(4, self.transponders[1]) ])

        self.assertFalse(result1.demand_not_fulfilled())
        self.assertFalse(result2.demand_not_fulfilled())

    def test_result_cost(self):
        demand = Demand(id=1, node1=1, node2=2, bitrate=100,
                        paths=[(100, [1, 2]), (14, [1, 3, 2])])

        result = Result(1, demand, 0, [(4, self.transponders[0]), (8, self.transponders[0]), (8, self.transponders[0])])

        self.assertEqual(result.cost(), 9)


if __name__ == '__main__':
    unittest.main()
