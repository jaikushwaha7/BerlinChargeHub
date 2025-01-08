# tests/test_search_station.py

import pytest
from ..src.domain.models import ChargingStation, Location
from .src.services import ChargingStationSearchService

def test_search_charging_stations():
    # Arrange: Create sample stations
    stations = [
        ChargingStation(name="Station A", location=Location(40.7128, -74.0060), types=["Fast"], is_available=True),
        ChargingStation(name="Station B", location=Location(40.73061, -73.935242), types=["Slow"], is_available=True),
        ChargingStation(name="Station C", location=Location(40.712776, -74.005974), types=["Fast"], is_available=False),
    ]

    # Create the search service
    search_service = ChargingStationSearchService(stations)

    # Act: Search for fast and available stations near a given location
    user_location = Location(40.7128, -74.0060)
    results = search_service.search(
        user_location=user_location,
        max_distance=10,
        charging_type="Fast",
        only_available=True
    )

    # Assert: Verify correct stations are returned
    assert len(results) == 1
    assert results[0].name == "Station A"
