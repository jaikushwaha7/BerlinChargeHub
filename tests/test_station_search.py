import pytest
from datetime import datetime
from src.application.services import ChargingStationSearchService
from src.infrastructure.repositories import MockStationRepository
from src.domain.events import StationSearchPerformed
from src.domain.exceptions import InvalidPostalCodeException

def test_search_stations_by_valid_postal_code():
    # Arrange
    postal_code = "10115"
    service = ChargingStationSearchService(MockStationRepository())

    # Act
    result = service.search_by_postal_code(postal_code)

    # Assert
    assert isinstance(result.event, StationSearchPerformed)
    assert len(result.stations) > 0
    assert all(station.is_in_postal_code(postal_code)
              for station in result.stations)

def test_invalid_berlin_postal_code():
    # Arrange
    service = ChargingStationSearchService(MockStationRepository())

    # Act & Assert
    with pytest.raises(InvalidPostalCodeException):
        service.search_by_postal_code("60306") # Other city code of Frankfurt am main