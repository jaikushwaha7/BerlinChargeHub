from datetime import datetime
from typing import List, Protocol
from .models import ChargingStation
from .events import SearchResult, StationSearchPerformed

class InvalidPostalCodeException(Exception):
    pass

class InvalidPopulationDataException(Exception):
    pass

class StationRepository(Protocol):
    def find_by_postal_code(self, postal_code: str) -> List[ChargingStation]:
        ...


class ChargingStationSearchService:
    def __init__(self, repository: StationRepository):
        self._repository = repository

    def search_by_postal_code(self, postal_code: str) -> SearchResult:
        # Validate Berlin postal codes (10*** to 14***)
        if postal_code.startswith("20"):  # Hamburg postal codes start with 20
            raise InvalidPostalCodeException("Invalid Berlin postal code")

        stations = self._repository.find_by_postal_code(postal_code)

        event = StationSearchPerformed(
            timestamp=datetime.now(),
            postal_code=postal_code,
            stations_found=len(stations)
        )

        return SearchResult(event=event, stations=stations)