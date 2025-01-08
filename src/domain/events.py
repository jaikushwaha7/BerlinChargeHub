from dataclasses import dataclass
from datetime import datetime
from typing import List
from .models import ChargingStation
from .value_objects import PostalCode, DemandScore

@dataclass
class StationSearchPerformed:
    timestamp: datetime
    postal_code: str
    stations_found: int

@dataclass
class SearchResult:
    event: StationSearchPerformed
    stations: List[ChargingStation]

@dataclass
class DemandScoreCalculated:
    timestamp: datetime
    postal_code: PostalCode
    demand_score: DemandScore

@dataclass
class DemandCalculationResult:
    event: DemandScoreCalculated
    postal_code: PostalCode
    demand_score: float