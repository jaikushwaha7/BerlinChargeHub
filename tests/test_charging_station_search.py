from unittest import TestCase
from unittest.mock import MagicMock, patch

import pandas as pd
from src.application.charging_station_search import SearchService
from src.domain.events.station_search_performed import StationSearchPerformed
from src.domain.models.charging_station import ChargingStation
from src.domain.value_objects.postal_code import PostalCode


class TestChargingStationSearch(TestCase):

    @patch("logging.warning")
    def test_search_by_postal_code_invalid_postal_code(self, mock_warning):
        search_service = SearchService()
        merged_df = pd.DataFrame()
        postal_code = "invalid_code"

        stations, search_summary = search_service.search_by_postal_code(merged_df, postal_code)

        self.assertEqual(stations, [])
        self.assertIsNone(search_summary)
        mock_warning.assert_called_once_with(f"Invalid postal code provided: {postal_code}")

    @patch("logging.info")
    def test_search_by_postal_code_no_results(self, mock_info):
        search_service = SearchService()
        merged_df = pd.DataFrame({
            "Postleitzahl": [10115, 10117],
            "Breitengrad": [52.5321, 52.5162],
            "Längengrad": [13.3849, 13.3893]
        })
        postal_code = "12345"

        stations, search_summary = search_service.search_by_postal_code(merged_df, postal_code)

        self.assertEqual(stations, [])
        self.assertEqual(search_summary.stations_found, 0)
        self.assertEqual(search_summary.postal_code, postal_code)
        mock_info.assert_any_call(f"Searching for postal code: {PostalCode(postal_code)}")

    @patch("logging.info")
    def test_search_by_postal_code_valid_results(self, mock_info):
        search_service = SearchService()
        merged_df = pd.DataFrame({
            "Postleitzahl": [10115, 12345],
            "Breitengrad": ["52.5321", "52.5200"],
            "Längengrad": ["13.3849", "13.4050"]
        })
        postal_code = "12345"

        stations, search_summary = search_service.search_by_postal_code(merged_df, postal_code)

        self.assertEqual(len(stations), 1)
        self.assertIsInstance(stations[0], ChargingStation)
        self.assertEqual(stations[0].postal_code, 12345)
        self.assertEqual(stations[0].latitude, 52.5200)
        self.assertEqual(stations[0].longitude, 13.4050)
        self.assertEqual(search_summary.stations_found, 1)
        mock_info.assert_any_call(f"Filtered dataframe:\n{merged_df[merged_df['Postleitzahl'] == int(postal_code)]}")

    @patch("logging.error")
    def test_search_by_postal_code_parsing_error(self, mock_error):
        search_service = SearchService()
        merged_df = pd.DataFrame({
            "Postleitzahl": [12345],
            "Breitengrad": ["invalid_value"],
            "Längengrad": ["13.4050"]
        })
        postal_code = "12345"

        stations, search_summary = search_service.search_by_postal_code(merged_df, postal_code)

        self.assertEqual(stations, [])
        self.assertEqual(search_summary.stations_found, 0)
        mock_error.assert_called()

    @patch("logging.error")
    def test_search_by_postal_code_unexpected_error(self, mock_error):
        search_service = SearchService()
        merged_df = None  # Force an unexpected error by passing None for DataFrame
        postal_code = "12345"

        stations, search_summary = search_service.search_by_postal_code(merged_df, postal_code)

        self.assertEqual(stations, [])
        self.assertIsNone(search_summary)
        mock_error.assert_called()
