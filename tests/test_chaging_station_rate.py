import pandas as pd
from src.application.chaging_station_rate import ChargeStationRating
from unittest import TestCase, mock
from unittest.mock import patch, MagicMock


class TestChargeStationRating(TestCase):

    @patch('streamlit.slider')
    @patch('streamlit.selectbox')
    @patch('streamlit.form_submit_button')
    @patch('streamlit.info')
    @patch('streamlit.success')
    @patch('sqlite3.connect')
    def test_charge_station_rating(self, mock_connect, mock_success, mock_info, mock_submit_button, mock_selectbox,
                                   mock_slider):
        # Define test data
        df_charging_stations = pd.DataFrame({
            'Postleitzahl': [10115, 10178, 13086],
            'Adresszusatz': ['Address 1', 'Address 2', 'Address 3']
        })
        df_merged_stations = pd.DataFrame({
            'PLZ': [10115, 10178],
            'Number': [1, 2]
        })

        mock_slider.return_value = 4
        mock_selectbox.side_effect = [10115, 'Address 1']
        mock_submit_button.return_value = True

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [4.0]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        obj = ChargeStationRating()
        obj.charge_station_rating(df_charging_stations, df_merged_stations)

        # Validate database operations
        mock_connect.assert_called_once_with('heatmap_app.db')
        mock_cursor.execute.assert_any_call(
            "INSERT INTO ratings (station_id, username, rating, timestamp) VALUES (?, ?, ?, ?)",
            ('Address 1', None, 4, mock.ANY)
        )
        mock_cursor.execute.assert_any_call(
            "SELECT AVG(rating) FROM ratings WHERE station_id = ?",
            ('Address 1',)
        )
        mock_connection.commit.assert_called()
        mock_connection.close.assert_called()

        # Validate Streamlit interactions
        mock_success.assert_called_with("Rating submitted for station Address 1")
        mock_info.assert_called_with("Average rating for station Address 1: 4.00")

    def test_rate_data_processing(self):
        # Define test data
        df_charging_stations = pd.DataFrame({
            'Postleitzahl': [10115, 10178, 13086, 9999, 15000],
            'Adresszusatz': ['Address 1', 'Address 2', 'Address 3', 'Address 4', None]
        })
        df_merged_stations = pd.DataFrame({
            'PLZ': [10115, 10178],
            'Number': [1, 0]
        })

        expected_output = pd.DataFrame({
            'PLZ': [10115],
            'Adresszusatz': ['Address 1']
        }).reset_index(drop=True)

        result = ChargeStationRating.rate_data_processing(df_charging_stations, df_merged_stations)
        pd.testing.assert_frame_equal(result, expected_output)
