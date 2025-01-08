from dataclasses import dataclass
from datetime import datetime

# Custom exceptions
class InvalidPostalCodeException(Exception):
    pass

class InvalidDemandScoreException(Exception):
    pass

@dataclass(frozen=True)
class PostalCode:
    value: str

    def __post_init__(self):
        if not self._is_valid_berlin_postal_code():
            raise InvalidPostalCodeException(
                f"{self.value} is not a valid postal code"
            )

    def _is_valid_berlin_postal_code(self) -> bool:
        return (self.value.startswith(("10", "12", "13")) and len(self.value) == 5)


@dataclass(frozen=True)
class DemandScore:
    value: float

    def __post_init__(self):
        if not 0 <= self.value <= 100:
            raise InvalidDemandScoreException(
                "Score should be between 0 and 100"
            )


@dataclass(frozen=True)
class DemandScoreCalculated:
    postal_code: str
    score: float
    population_density: int
    existing_stations: int
    timestamp: datetime


class DemandIndicatorService:
    def __init__(self, station_repository, population_repository):
        self.station_repository = station_repository
        self.population_repository = population_repository

    def calculate_demand_score(self, postal_code: str, population_data: dict) -> DemandScoreCalculated:
        # Validate postal code
        postal_code = PostalCode(postal_code)

        # Retrieve station data
        existing_stations = len(
            self.station_repository.find_by_postal_code(postal_code)
        )

        # Retrieve population data
        population_density = population_data.get("density", 0)
        ev_percentage = population_data.get("ev_percentage", 0)

        # Calculate demand score
        demand_score = min(100, max(0, population_density * ev_percentage * 10))

        return DemandScoreCalculated(
            postal_code=postal_code.value,
            score=demand_score,
            population_density=population_density,
            existing_stations=existing_stations,
            timestamp=datetime.now(),
        )
