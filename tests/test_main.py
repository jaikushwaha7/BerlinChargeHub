from unittest import TestCase
from unittest.mock import patch, MagicMock
import logging
import pandas as pd
from main import main


class TestMain(TestCase):
    @patch('main.pd.read_csv')
    @patch('main.m1.preprop_lstat')
    @patch('main.m1.count_plz_occurrences')
    @patch('main.m1.preprop_resid')
    @patch('main.m1.make_streamlit_electric_Charging_resid')
    @patch('logging.info')
    @patch('logging.error')
    def test_main_success(self, mock_error, mock_info, mock_streamlit_function, mock_preprop_resid,
                          mock_count_plz_occurrences, mock_preprop_lstat, mock_read_csv):
        # Mock the pd.read_csv function to return a DataFrame
        mock_read_csv.side_effect = [
            pd.DataFrame({'column': ['value1', 'value2']}),  # Mock for geodata_berlin_plz.csv
            pd.DataFrame({'column': ['value3', 'value4']}),  # Mock for Ladesaeulenregister.csv
            pd.DataFrame({'column': ['value5', 'value6']})   # Mock for plz_einwohner.csv
        ]

        # Mock preprop_lstat and preprop_resid to return dummy data
        mock_preprop_lstat.return_value = pd.DataFrame({'processed_col': [1, 2]})
        mock_count_plz_occurrences.return_value = MagicMock()
        mock_preprop_resid.return_value = MagicMock()

        # Call the 'main' function
        main()

        # Assertions for successful execution
        mock_read_csv.assert_any_call(f'{main.currentWorkingDirectory}\\datasets\\geodata_berlin_plz.csv', delimiter=';')
        mock_read_csv.assert_any_call(f'{main.currentWorkingDirectory}\\datasets\\Ladesaeulenregister.csv', delimiter=';')
        mock_read_csv.assert_any_call(f'{main.currentWorkingDirectory}\\datasets\\plz_einwohner.csv')

        mock_preprop_lstat.assert_called_once()
        mock_count_plz_occurrences.assert_called_once()
        mock_preprop_resid.assert_called_once()
        mock_streamlit_function.assert_called_once()

        # Ensure logging captured successful file loads
        mock_info.assert_any_call("geodata_berlin_plz.csv loaded successfully.")
        mock_info.assert_any_call("Ladesaeulenregister.csv loaded successfully.")
        mock_info.assert_any_call("plz_einwohner.csv loaded successfully.")
        mock_error.assert_not_called()

    @patch('main.pd.read_csv')
    @patch('logging.error')
    def test_main_geodata_load_error(self, mock_logging_error, mock_read_csv):
        # Mock read_csv to raise an exception for the first file
        mock_read_csv.side_effect = [Exception("File not found")]

        # Verify that the main function raises an exception
        with self.assertRaises(Exception):
            main()

        # Ensure logging captured the error
        mock_logging_error.assert_called_once_with("Failed to load geodata_berlin_plz.csv: File not found")

    @patch('main.pd.read_csv')
    @patch('logging.error')
    def test_main_lstat_load_error(self, mock_logging_error, mock_read_csv):
        # Mock read_csv to succeed for the first file and fail for the second
        mock_read_csv.side_effect = [
            pd.DataFrame({'column': ['value1', 'value2']}),  # Mock for geodata_berlin_plz.csv
            Exception("File not found")
        ]

        # Verify that the main function raises an exception
        with self.assertRaises(Exception):
            main()

        # Ensure logging captured the error for the second file
        mock_logging_error.assert_called_once_with("Failed to load Ladesaeulenregister.csv: File not found")

    @patch('main.pd.read_csv')
    @patch('logging.error')
    def test_main_residents_load_error(self, mock_logging_error, mock_read_csv):
        # Mock read_csv to succeed for the first two files and fail for the third
        mock_read_csv.side_effect = [
            pd.DataFrame({'column': ['value1', 'value2']}),  # Mock for geodata_berlin_plz.csv
            pd.DataFrame({'column': ['value3', 'value4']}),  # Mock for Ladesaeulenregister.csv
            Exception("File not found")
        ]

        # Verify that the main function raises an exception
        with self.assertRaises(Exception):
            main()

        # Ensure logging captured the error for the third file
        mock_logging_error.assert_called_once_with("Failed to load plz_einwohner.csv: File not found")
