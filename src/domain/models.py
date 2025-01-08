from dataclasses import dataclass
from typing import List
from .value_objects import PostalCode, DemandScore

@dataclass
class ChargingStation:
    id: str
    name: str
    postal_code: str
    latitude: float
    longitude: float

    def is_in_postal_code(self, postal_code: str) -> bool:
        return self.postal_code == postal_code

@dataclass
class PopulationData:
    density: int
    ev_percentage: float

@dataclass
class DemandIndicator:
    postal_code: PostalCode
    population_data: PopulationData
    demand_score: DemandScore