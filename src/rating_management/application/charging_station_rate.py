import sqlite3
from datetime import datetime
from src.utils import logger as lg
import streamlit as st
from src.rating_management.model.rating import Rating
from src.rating_management.events.rating_avg_calculated import RatingAverageCalculated

@lg.logger_decorator
class ChargeStationRating:

    def __init__(self, db_path='heatmap_app.db'):
        self.db_path = db_path

    def charge_station_rating(self, df_charging_stations, df_merged_stations, avg_rating=None):
        """
        Collects and submits user ratings for selected charging stations, calculates, and
        displays the average rating for the selected charging station.
        """
        # Preprocess data for display
        global rating
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
        rating = []
        # Submit button within form
        if st.button("Submit Rating"):
            # Save rating to database
            self.save_rating(selected_station, rating_value)
            rating = Rating(
                                        user_id =  st.session_state.username,
                                        station_postal_code =  st.session_state.selected_plz,
                                        station_address = st.session_state.selected_station,
                                        stars = rating_value )

        # Calculate and display average rating
        if selected_station:
            self.display_average_rating(selected_station)

            if avg_rating is not None:
                # Create RatingAverageCalculated object
                rating_average_calculated = RatingAverageCalculated(
                    station_postal_code=st.session_state.selected_plz,
                    station_address=selected_station,
                    rating_average=avg_rating
                )



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
            return avg_rating  # Return the calculated average rating
        else:
            st.info(f"No ratings yet for station: {station}")
            return None  # Return None if no ratings exist
