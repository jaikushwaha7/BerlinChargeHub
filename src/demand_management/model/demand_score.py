from dataclasses import dataclass
from src.search_management.value_objects.postal_code import PostalCode
from src.demand_management.value_objects.score import Score

@dataclass
class DemandScore:
    """
    Represents a charging station with location information.
    """
    demand_score: Score
    postal_code: PostalCode

