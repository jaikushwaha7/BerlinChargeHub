import pytest
from src.application.services import DemandIndicatorService
from src.infrastructure.repositories import (
    MockStationRepository,
    MockPopulationRepository
)
from src.domain.events import DemandScoreCalculated
from src.domain.exceptions import InvalidPostalCodeException

def test_calculate_demand_score_for_area():
    # Arrange
    postal_code = "10115"
    population_data = {"density": 5000, "ev_percentage": 0.15}
    service = DemandIndicatorService(
        MockStationRepository(),
        MockPopulationRepository()
    )

    # Act
    result = service.calculate_demand_score(postal_code, population_data)

    # Assert
    assert isinstance(result.event, DemandScoreCalculated)
    assert 0 <= result.demand_score <= 100
    assert result.postal_code.value == postal_code

def test_invalid_postal_code_for_demand():
    # Arrange
    service = DemandIndicatorService(
        MockStationRepository(),
        MockPopulationRepository()
    )

    # Act & Assert
    with pytest.raises(InvalidPostalCodeException):
        service.calculate_demand_score("99999", {})