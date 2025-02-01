
import logging

import folium
import pandas
import streamlit as st
from streamlit_folium import folium_static

import src.utils.logger as lg
from src.domain.events.station_search_performed import StationSearchPerformed
from src.domain.models.charging_station import ChargingStation
from src.domain.value_objects.postal_code import PostalCode


@lg.logger_decorator
class SearchService:
    def search_by_postal_code(merged_df: pandas.DataFrame, plz: str) -> tuple[
        list[ChargingStation], StationSearchPerformed]:
        logging.info("search_by_postal_code method called.")

        """
            Searches the dataframe for stations by a given postal code.

            :param merged_df:
            :param postal_code: The postal code to search for (string, int, or float).
            :return: A list of station dictionaries with name, status, and location.
            """
        try:

            logging.info("Starting postal code validation.")
            # Validate the postal code
            logging.info("Finished postal code validation.")
            if plz is None or not str(plz).strip().replace('.', '', 1).isdigit():
                logging.warning(f"Invalid postal code provided: {plz}")
                st.error("Invalid postal code provided.")

            # Convert postal code to PostalCode
            plz = int(float(PostalCode(plz).value))

            logging.info(f"Searching for postal code: {plz}")
            print(f"Postal Code (plz): {plz}, Type: {type(plz)}")

            merged_df = merged_df.astype({"PLZ": int})
            logging.info(f"merged_df: \n{merged_df.head()}")

            print(f"Looking for PLZ: {plz}")
            print(merged_df["PLZ"].unique())

            logging.info("Filtering the dataframe based on the provided postal code.")
            # Filter the dataframe for the given postal code
            logging.info("Finished filtering the dataframe.")
            filtered_df = merged_df[merged_df["PLZ"] == plz]
            logging.info(f"Filtered dataframe:\n{filtered_df.head()}")
            if filtered_df.empty:
                logging.warning(f"No locations found for postal code: {plz}")
                return [], StationSearchPerformed(
                    timestamp=pandas.Timestamp.now(),
                    postal_code=str(plz),
                    stations_found=0
                )

            logging.info("Converting filtered station data to ChargingStation objects.")
            # Prepare the list of stations
            stations = []
            for _, row in filtered_df.iterrows():
                try:
                    lat = float(str(row["Breitengrad"]).replace(',', '.'))
                    lon = float(str(row["Längengrad"]).replace(',', '.'))
                    stations.append(ChargingStation(
                        postal_code=row["PLZ"],
                        latitude=lat,
                        longitude=lon
                    ))
                except ValueError as e:
                    logging.error(f"Error parsing location for row: {row}\n{e}")
            search_summary = None
            search_summary = StationSearchPerformed(
                timestamp=pandas.Timestamp.now(),
                postal_code=str(plz),
                stations_found=int(filtered_df['Number'].iloc[0])
            )
            
            return stations, search_summary

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return []


# def display_folium_map(filtered_stations, folium_static):
#
#     logging.info(f"display_folium_map called with {len(filtered_stations)} stations to display.")
#     if filtered_stations.empty:
#         st.error("No charging station data available to display on the map.")
#         return
#
#     # Initialize map centered on the first station
#     first_station = filtered_stations.iloc[0]
#
#     for _, station in first_station.iterrows():
#         folium.Marker(
#             location=[station["Breitengrad"], station["Längengrad"]],
#             popup=f'Station at Postal code: {station["PLZ"]}',
#             icon=folium.Icon(icon='cloud')
#         ).add_to(folium_static)
#
#     # Display the map in Streamlit
#     return folium_static
#

# def search_by_postal_code(plz, residents_df, stations_df):
#     filtered_residents = filter_dataframe_by_postal_code(residents_df, plz)
#     filtered_stations = filter_dataframe_by_postal_code(stations_df, plz)
#
#     display_search_results(plz, filtered_residents, filtered_stations)
#     display_folium_map(filtered_stations)
#
#
# def filter_dataframe_by_postal_code(df, plz):
#     return df[df['PLZ'].astype(str) == plz]
#
#
# def display_search_results(plz, filtered_residents, filtered_stations):
#     if not filtered_stations.empty :
#         st.write("Search Results:")
#         st.write("Charging Stations Data:")
#         st.write(filtered_stations)
#     else:
#         st.error(f"No data found for Postal Code: {plz}")
#
#
