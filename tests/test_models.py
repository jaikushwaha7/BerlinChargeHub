import unittest

from src.domain.models import ChargingStation


class TestChargingStation(unittest.TestCase):
    """Test cases for ChargingStation class"""

    def test_is_in_postal_code_matches(self):
        """Test if the postal code matches the charging station's postal code"""
        station = ChargingStation(
            id="1",
            name="Test Station",
            postal_code="12345",
            latitude=50.0,
            longitude=10.0,
        )
        self.assertTrue(station.is_in_postal_code("12345"))

    def test_is_in_postal_code_does_not_match(self):
        """Test if the postal code does not match the charging station's postal code"""
        station = ChargingStation(
            id="1",
            name="Test Station",
            postal_code="12345",
            latitude=50.0,
            longitude=10.0,
        )
        self.assertFalse(station.is_in_postal_code("67890"))


if __name__ == "__main__":
    unittest.main()
