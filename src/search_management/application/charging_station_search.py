
import logging

import pandas
import streamlit as st

import src.utils.logger as lg
from src.search_management.events.station_search_performed import StationSearchPerformed
from src.search_management.model.charging_station import ChargingStation
from src.search_management.value_objects.postal_code import PostalCode


@lg.logger_decorator
class SearchService:
    def search_by_postal_code(self, merged_df: pandas.DataFrame, plz: str) -> tuple[
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

            merged_df = merged_df.astype({"PLZ": int})
            logging.info(f"merged_df: \n{merged_df.head()}")

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
                        postal_code=str(row["PLZ"]),
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