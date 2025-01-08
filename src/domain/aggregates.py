from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .value_objects import PostalCode, DemandScore
from .events import DemandScoreCalculated


@dataclass
class Area:
    """
    Area Aggregate Root
    Represents a geographical area defined by postal code and contains population metrics
    """
    postal_code: PostalCode
    population_density: int
    ev_adoption_rate: float
    _demand_score: Optional[DemandScore] = None
    _stations: List['ChargingStation'] = None

    def calculate_demand_score(self) -> DemandScoreCalculated:
        # Calculate demand based on area characteristics
        base_score = min(self.population_density / 100, 50)
        ev_score = self.ev_adoption_rate * 100 * 0.5
        total_score = min(base_score + ev_score, 100)

        self._demand_score = DemandScore(total_score)

        return DemandScoreCalculated(
            timestamp=datetime.now(),
            postal_code=self.postal_code,
            demand_score=self._demand_score
        )

    def add_station(self, station: 'ChargingStation') -> None:
        if station.postal_code != self.postal_code:
            raise ValueError("Station postal code must match area postal code")
        if self._stations is None:
            self._stations = []
        self._stations.append(station)

    @property
    def station_count(self) -> int:
        return len(self._stations) if self._stations else 0

    @property
    def demand_score(self) -> Optional[DemandScore]:
        return self._demand_score


@dataclass
class ChargingStation:
    """
    ChargingStation Entity
    Part of the Area aggregate
    """
    id: str
    name: str
    postal_code: PostalCode
    latitude: float
    longitude: float
    status: str