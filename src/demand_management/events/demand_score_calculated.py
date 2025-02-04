from dataclasses import dataclass
from src.demand_management.value_objects.score import Score
from src.search_management.value_objects.postal_code import PostalCode

@dataclass
class DemandScoreCalculated:
    postal_code: PostalCode
    demand_score: Score


