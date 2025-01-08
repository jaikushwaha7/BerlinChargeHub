import unittest
from src.utils.postal_code_validator import PostalCodeValidator
from src.models.location import Location
from src.models.charging_station import ChargingStation
from src.services.station_finder import StationFinder

class TestPostalCodeValidator(unittest.TestCase):
    def test_valid_berlin_postal_code(self):
        stations = [
            ChargingStation('12345', Location(52.5200, 13.4050), 4),
            ChargingStation('12355', Location(52.5300, 13.4150), 2),
            ChargingStation('10245', Location(52.5300, 13.4150), 2),
        ]        
        finder = StationFinder(stations)
        user_postal_code = finder.find_stations_by_postal_code('10245')
        # Valid Berlin postal codes
        self.assertTrue(PostalCodeValidator.is_valid_berlin_postal_code("10115"))
        self.assertTrue(PostalCodeValidator.is_valid_berlin_postal_code("14199"))
        self.assertTrue(PostalCodeValidator.is_valid_berlin_postal_code(user_postal_code[0].postal_code))

    def test_invalid_berlin_postal_code(self):
        # Invalid Berlin postal codes
        self.assertFalse(PostalCodeValidator.is_valid_berlin_postal_code("00000"))  # Too low
        self.assertFalse(PostalCodeValidator.is_valid_berlin_postal_code("14200"))  # Too high
        self.assertFalse(PostalCodeValidator.is_valid_berlin_postal_code("1234"))   # Too short
        self.assertFalse(PostalCodeValidator.is_valid_berlin_postal_code("123456")) # Too long
        self.assertFalse(PostalCodeValidator.is_valid_berlin_postal_code("ABCDE"))  # Non-numeric

if __name__ == "__main__":
    unittest.main()