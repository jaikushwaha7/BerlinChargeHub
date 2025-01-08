from typing import List
from .models import ChargingStation

class MockStationRepository:
    def find_by_postal_code(self, postal_code: str) -> List[ChargingStation]:
        # Mock data for testing
        return [
            ChargingStation(
                id="1",
                name="Test Station 1",
                postal_code=postal_code,
                latitude=52.5200,
                longitude=13.4050
            ),
            ChargingStation(
                id="2",
                name="Test Station 2",
                postal_code=postal_code,
                latitude=52.5200,
                longitude=13.4050
            )
        ]