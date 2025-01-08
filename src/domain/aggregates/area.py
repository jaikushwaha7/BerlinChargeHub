from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from src.domain.value_objects import postal_code

from src.domain.models.charging_station import ChargingStation

@dataclass
class Area:
    """
    Area Aggregate Root
    Represents a geographical area defined by postal code and contains population metrics
    """
    postal_code: postal_code.PostalCode
    population_density: int
    number_of_charging_stations: int = 0
    _demand_score: Optional[DemandScore] = None
    _stations: List['ChargingStation'] = None


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