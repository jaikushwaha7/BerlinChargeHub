import unittest
from src.domain.models.charging_station import Location
from src.domain.models.charging_station import ChargingStation
from src.application.charging_station_search import SearchService

class TestStationFinder(unittest.TestCase):
    def test_find_nearby_stations(self):
        # Arrange 
        stations = [
            ChargingStation('12345', Location(52.5200, 13.4050), 4),
            ChargingStation('12355', Location(52.5300, 13.4150), 2),
            ChargingStation('10245', Location(52.5300, 13.4150), 2),
        ]
        finder = SearchService(stations)
        user_postal_code = finder.search_by_postal_code('10245')
        user_location = Location(52.5200, 13.4050)

        # Act
        nearby_stations = finder.find_nearby_stations(user_location, radius=0.1)

        # Assert
        self.assertEqual(len(nearby_stations), 3)
        self.assertEqual(nearby_stations[0].postal_code, '12345')

##################################################################################

    def test_find_stations_by_postal_code(self):
        # Arrange 
        stations = [
            ChargingStation('10318', Location(52.5200, 13.4050), 4),
            ChargingStation('10115', Location(52.5300, 13.4150), 2),
            ChargingStation('10245', Location(52.5300, 13.4150), 2),
        ]
        finder = StationFinder(stations)
        # Find stations in postal code 10115
        result = finder.find_stations_by_postal_code("10115")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].postal_code, "10115")

        # Find stations in postal code 10318
        result = finder.find_stations_by_postal_code("10318")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].postal_code, "10318")

        # Find stations in a non-existent postal code
        result = finder.find_stations_by_postal_code("00000")
        self.assertEqual(len(result), 0)

 

if __name__ == "__main__":
    unittest.main()