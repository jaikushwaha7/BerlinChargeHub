# File: tests/test_repositories.py

import unittest
from unittest.mock import patch

from src.domain.models import ChargingStation
from src.infrastructure.repositories import MockStationRepository


class TestSampleData(unittest.TestCase):
    @patch("src.infrastructure.repositories.ChargingStation")
    def test_sample_data_valid_postal_code(self, mock_charging_station):
        # Arrange
        repository = MockStationRepository()
        mock_charging_station.return_value = ChargingStation(
            
            postal_code="10115",
            latitude=52.5200,
            longitude=13.4050
        )

        # Act
        result = repository.sample_data("10115")

        # Assert
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(item, ChargingStation) for item in result))
        self.assertEqual(result[0].postal_code, "10115")
        self.assertEqual(result[1].postal_code, "10115")

    @patch("src.infrastructure.repositories.ChargingStation")
    def test_sample_data_empty_postal_code(self, mock_charging_station):
        # Arrange
        repository = MockStationRepository()

        # Act
        result = repository.sample_data("")

        # Assert
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(item, ChargingStation) for item in result))
        self.assertEqual(result[0].postal_code, "")
        self.assertEqual(result[1].postal_code, "")

    @patch("src.infrastructure.repositories.ChargingStation")
    def test_sample_data_invalid_postal_code_format(self, mock_charging_station):
        # Arrange
        repository = MockStationRepository()

        # Act
        result = repository.sample_data("InvalidCode123")

        # Assert
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(item, ChargingStation) for item in result))
        self.assertEqual(result[0].postal_code, "InvalidCode123")
        self.assertEqual(result[1].postal_code, "InvalidCode123")


if __name__ == "__main__":
    unittest.main()
