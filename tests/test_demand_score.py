from src.domain.value_objects.demand_score import DemandScore
from unittest import TestCase

class TestDemandScore(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDemandScore, self).__init__(*args, **kwargs)
    def test_demand_score_is_number(self, demand_score = DemandScore):

        self.assertIsInstance(demand_score, (int, float), "demand_score must be a number")

    def test_demand_score_not_infinite(self,demand_score = DemandScore):
        self.assertNotEqual(demand_score, float('inf'), "demand_score must not be positive infinity")
        self.assertNotEqual(demand_score, float('-inf'), "demand_score must not be negative infinity")
