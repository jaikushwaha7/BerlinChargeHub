from typing import List
from src.domain.models import ChargingStation

class MockStationRepository:
    def sample_data(self, postal_code: str) -> List[ChargingStation]:
        # Mock data for testing
        return [
            ChargingStation(
                postal_code=postal_code,
                latitude=52.5200,
                longitude=13.4050
            ),
            ChargingStation(
                postal_code=postal_code,
                latitude=52.5200,
                longitude=13.4050
            )
        ]

class MockPopulationRepository:
    def sample_population(self, postal_code: str):
        return 100