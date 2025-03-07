import sqlite3
from datetime import datetime
from src.utils import logger as lg
import streamlit as st

from src.domain.models.rating_system import Rating

@lg.logger_decorator
class ChargeStationRating:

    def __init__(self, db_path='heatmap_app.db'):
        self.db_path = db_path

    def charge_station_rating(self, df_charging_stations, df_merged_stations):
        """
        Collects and submits user ratings for selected charging stations, calculates, and
        displays the average rating for the selected charging station.
        """
        # Preprocess data for display
        df_charging_stations = self.rate_data_processing(df_charging_stations, df_merged_stations)

        # Extract unique postal codes
        plz_list = df_charging_stations['PLZ'].unique().astype(int)

        # Select postal code (updates dynamically)
        st.selectbox("Select Postal Code:", plz_list, key="selected_plz")

        # Dynamically update the list of stations based on selected PLZ
        if 'selected_plz' in st.session_state:
            station_list = df_charging_stations[df_charging_stations['PLZ'] == st.session_state.selected_plz][
                'Adresszusatz'].unique()
        else:
            station_list = []

        # Select station from dynamically updated list
        selected_station = st.selectbox("Select Charging Station:", station_list, key="selected_station")

        # Rating slider
        rating_value = st.slider("Rating (1-5):", 1, 5, 3)

        # Submit button within form
        if st.button("Submit Rating"):
            # Save rating to database
            self.save_rating(selected_station, rating_value)

        # Calculate and display average rating
        if selected_station:
            self.display_average_rating(selected_station)

    @staticmethod
    def rate_data_processing(df_charging_stations, df_merged_stations):
        """
        Processes charging station data and filters based on conditions.
        """
        df_charging_stations = df_charging_stations.loc[:, ['Postleitzahl', 'Adresszusatz']].drop_duplicates(
            subset=['Adresszusatz'])
        df_charging_stations = df_charging_stations.dropna(subset=['Adresszusatz'])
        df_charging_stations = df_charging_stations.reset_index(drop=True)
        df_charging_stations = df_charging_stations.rename(columns={'Postleitzahl': 'PLZ'})

        df_charging_stations = df_charging_stations[
            (df_charging_stations["PLZ"] > 10000) &
            (df_charging_stations["PLZ"] < 14200)]
        df_merged_stations = df_merged_stations[df_merged_stations['Number'] > 0]

        df_charging_stations = df_charging_stations.loc[df_charging_stations['PLZ'].isin(df_merged_stations['PLZ'])]

        return df_charging_stations

    def save_rating(self, station, rating):
        """
        Saves the user rating to the database.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO ratings (station_id, username, rating, timestamp) VALUES (?, ?, ?, ?)",
            (station, st.session_state.username, rating, datetime.now())
        )
        conn.commit()
        conn.close()
        st.success(f"Rating submitted for station: {station}")

    def display_average_rating(self, station):
        """
        Displays the average rating of a specific station.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT AVG(rating) FROM ratings WHERE station_id = ?",
            (station,)
        )
        avg_rating = c.fetchone()[0]
        conn.close()
        if avg_rating:
            st.info(f"Average rating for station {station}: {avg_rating:.2f}")
        else:
            st.info(f"No ratings yet for station: {station}")
    # def __init__(self, db_path='heatmap_app.db'):
    #     self.db_path = db_path
    #
    # def charge_station_rating(self, df_charging_stations, df_merged_stations):
    #     """
    #     Collects and submits user ratings for selected charging stations, calculates, and
    #     displays the average rating for the selected charging station.
    #     """
    #     with st.form("rating_form"):
    #         df_charging_stations = self.rate_data_processing(df_charging_stations, df_merged_stations)
    #         plz_list = df_charging_stations['PLZ'].unique().astype(int)
    #         selected_plz = st.selectbox("Select Postal Code:", plz_list, key="selected_plz")
    #         station_list = df_charging_stations[df_charging_stations['PLZ'] == st.session_state.selected_plz]['Adresszusatz'].unique()
    #
    #         selected_station = st.selectbox("Select Charging Station:", station_list)
    #         rating_value = st.slider("Rating (1-5):", 1, 5, 3)
    #         submit_rating = st.form_submit_button("Submit Rating")
    #
    #         if submit_rating:
    #             rating = Rating(
    #                 id=None,  # This will usually be generated by the database
    #                 user_id=st.session_state.username,
    #                 station_id=selected_station,
    #                 stars=rating_value,
    #                 review=None  # Placeholder for optional review if needed
    #             )
    #             conn = sqlite3.connect(self.db_path)
    #             c = conn.cursor()
    #             c.execute(
    #                 "INSERT INTO ratings (station_id, username, rating, timestamp) VALUES (?, ?, ?, ?)",
    #                 (rating.station_id, rating.user_id, rating.stars, datetime.now())
    #             )
    #             conn.commit()
    #             conn.close()
    #             st.success(f"Rating submitted for station {rating.station_id}")
    #     # Calculate and display average rating
    #     conn = sqlite3.connect(self.db_path)
    #     c = conn.cursor()
    #     c.execute(
    #         "SELECT AVG(rating) FROM ratings WHERE station_id = ?",
    #         (selected_station,)
    #     )
    #     avg_rating = c.fetchone()[0]
    #     conn.close()
    #     if avg_rating:
    #         st.info(f"Average rating for station {selected_station}: {avg_rating:.2f}")
    #
    # @staticmethod
    # def rate_data_processing(df_charging_stations, df_merged_stations):
    #     """
    #     Processes and filters the given DataFrame of charging stations based on specific
    #     criteria such as duplication, missing data, and postal code range. The function
    #     removes duplicate rows based on 'Adresszusatz', filters out rows with missing
    #     values in 'Adresszusatz', and renames the column 'Postleitzahl' to 'PLZ'. Finally,
    #     it keeps only the rows where 'PLZ' falls within the range of 10000 to 14200.
    #
    #     """
    #     df_charging_stations = df_charging_stations.loc[:, ['Postleitzahl', 'Adresszusatz']].drop_duplicates(subset=['Adresszusatz'])
    #     df_charging_stations = df_charging_stations.dropna(subset=['Adresszusatz'])
    #     df_charging_stations = df_charging_stations.reset_index(drop=True)
    #     df_charging_stations = df_charging_stations.rename(columns={'Postleitzahl': 'PLZ'})
    #
    #     df_charging_stations = df_charging_stations[
    #         (df_charging_stations["PLZ"] > 10000) &
    #         (df_charging_stations["PLZ"] < 14200)]
    #     df_merged_stations = df_merged_stations[df_merged_stations['Number'] > 0]
    #
    #     df_charging_stations = df_charging_stations.loc[df_charging_stations['PLZ'].isin(df_merged_stations['PLZ'])]
    #
    #     return df_charging_stations
    #
    #
    #
