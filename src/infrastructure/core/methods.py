from datetime import datetime
import logging
from dbm import sqlite3

import folium
import geopandas as gpd
from pandas import merge
from folium.plugins import HeatMap
import streamlit as st
# from branca.colormap import LinearColormap
from streamlit_folium import folium_static

import src.infrastructure.core.HelperTools as ht
from src.application.charging_station_search import SearchService
from src.application.demand_calculator import DemandCalculator
from src.application.login import handle_login  # Import the login function
from src.application.mapping import mapping_residents, mapping_stations, mapping_demand
from src.exceptions.exceptions import LoginException, SearchException
from src.utils import logger as lg
from src.utils.database_utils import verify_user

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def sort_by_plz_add_geometry(dfr, dfg, pdict):
    """
    Sorts a DataFrame by 'PLZ', merges it with a GeoDataFrame based on a provided key,
    and converts the geometry column to a GeoSeries, resulting in a GeoDataFrame.

    """
    logger.info("Starting sort_by_plz_add_geometry function.")
    logger.debug(f"Input DataFrame shape: {dfr.shape}, Geo DataFrame shape: {dfg.shape}, Parameters: {pdict}")
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()

    logger.debug(f"DataFrame initial state: {dframe.shape}")
    logger.debug(f"Geo DataFrame initial state: {df_geo.shape}")
    
    sorted_df               = dframe\
        .sort_values(by='PLZ')\
        .reset_index(drop=True)\
        .sort_index()
    logger.debug(f"Sorted DataFrame shape: {sorted_df.shape}")
        
    sorted_df2              = sorted_df.merge(df_geo, on=pdict["geocode"], how ='left')
    logger.info(f"Merged DataFrame with geometry. Shape: {sorted_df2.shape}")
    logger.debug(f"First 5 rows of merged DataFrame:\n{sorted_df2.head(5)}")
    
    sorted_df3              = sorted_df2.dropna(subset=['geometry'])
    logger.info(f"DataFrame after dropping missing geometries. Shape: {sorted_df3.shape}")
    logger.debug(f"First 5 rows after dropping missing geometries:\n{sorted_df3.head(5)}")
    
    sorted_df3['geometry']  = gpd.GeoSeries.from_wkt(sorted_df3['geometry'])
    ret                     = gpd.GeoDataFrame(sorted_df3, geometry='geometry')
    
    logger.info("sort_by_plz_add_geometry function completed successfully.")
    return ret

# -----------------------------------------------------------------------------
@ht.timer
def preprop_lstat(dfr, dfg, pdict):
    """Preprocessing dataframe from Ladesaeulenregister.csv"""
    logger.info("Starting preprop_lstat function.")
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    
    logger.debug(f"Input DataFrame shape: {dframe.shape}")
    logger.debug(f"Geo DataFrame shape: {df_geo.shape}")
    
    dframe2               	= dframe.loc[:,['Postleitzahl', 'Bundesland', 'Breitengrad', 'Längengrad', 'Nennleistung Ladeeinrichtung [kW]']]
    logger.debug(f"Initial DataFrame subset for preprocessing:\n{dframe2.head(5)}")
    dframe2.rename(columns  = {"Nennleistung Ladeeinrichtung [kW]":"KW", "Postleitzahl": "PLZ"}, inplace = True)
    logger.info("Renamed columns in DataFrame.")

    # Convert to string and replace commas with periods
    for col in ['Breitengrad', 'Längengrad']:
        dframe2[col] = dframe2[col].astype(str).str.replace(',', '.')
    logger.info("Formatted latitude and longitude columns.")

    # Filtering Berlin postal codes
    dframe3                 = dframe2[(dframe2["Bundesland"] == 'Berlin') &
                                            (dframe2["PLZ"] > 10115) &  
                                            (dframe2["PLZ"] < 14200)]
    logger.info(f"Filtered data for Berlin. Shape: {dframe3.shape}")
    logger.debug(f"First 5 rows of filtered DataFrame:\n{dframe3.head(5)}")
    
    ret = sort_by_plz_add_geometry(dframe3, df_geo, pdict)
    
    logger.info("preprop_lstat function completed successfully.")
    return ret
    

# -----------------------------------------------------------------------------
@ht.timer
def count_plz_occurrences(df_lstat2):
    """Counts loading stations per PLZ"""
    logger.info("Starting count_plz_occurrences function.")
    logger.debug(f"Input DataFrame shape: {df_lstat2.shape}")

    # Group by PLZ and count occurrences, keeping geometry
    result_df = df_lstat2.groupby('PLZ').agg(
        Number=('PLZ', 'count'),
        geometry=('geometry', 'first')
    ).reset_index()

    logger.info(f"count_plz_occurrences function completed successfully. Output DataFrame shape: {result_df.shape}")
    logger.debug(f"First 5 rows of the output DataFrame:\n{result_df.head(5)}")

    return result_df
    
# -----------------------------------------------------------------------------


@ht.timer
def preprop_resid(dfr, dfg, pdict):
    """
    Processes and prepares a dataframe by cleaning and filtering postal codes, renaming columns, and transforming
    geographical data. The function works by copying the given data, transforming numeric columns into strings, and replacing
    comma-separators for proper formatting. It also filters the dataset based on postal codes and combines additional
    geometry information via another function.

    Return: The processed dataframe with cleaned, formatted, and enriched data combining postal codes and geometrical information.
    :rtype: pandas.DataFrame
    """
    logger.info("Starting preprop_resid function.")
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    logger.debug(f"Input DataFrame shape: {dframe.shape}, Geo DataFrame shape: {df_geo.shape}")

    dframe2               	= dframe.loc[:,['plz', 'einwohner', 'lat', 'lon']]
    dframe2.rename(columns  = {"plz": "PLZ", "einwohner": "Einwohner", "lat": "Breitengrad", "lon": "Längengrad"}, inplace = True)
    logger.info("Renamed columns in DataFrame.")
    # Convert to string
    for col in ['Breitengrad', 'Längengrad']:
        dframe2[col] = dframe2[col].astype(str).str.replace(',', '.')
    logger.info("Formatted latitude and longitude columns.")
    
    # Filtering Berlin postal codes
    dframe3                 = dframe2[
                                            (dframe2["PLZ"] > 10000) &
                                            (dframe2["PLZ"] < 14200)]
    logger.info(f"Filtered DataFrame by postal codes. Remaining rows: {dframe3.shape[0]}")
    logger.debug(f"First 5 rows of the filtered DataFrame:\n{dframe3.head(5)}")

    ret = sort_by_plz_add_geometry(dframe3, df_geo, pdict)
    logger.info("preprop_resid function completed successfully.")
    return ret

# -----------------------------------------------------------------------------
@ht.timer
def merge_geo_dataframes(df_charging_stations, df_population):
    '''
    Merges the charging stations and population dataframes and fills NA's with 0
    Inputs:
        - df_charging_stations: A geodataframe sorted by PLZ and containing information about the charging stations
        - df_population: A geodataframe sorted by PLZ and containing information about the population
    Outputs: A merged geodataframe
    '''
    logger.info("Starting merge_geo_dataframes function.")
    logger.debug(f"Charging Stations DataFrame shape: {df_charging_stations.shape}, Population DataFrame shape: {df_population.shape}")

    # Merge resident and charging station data
    df_charging_stations['PLZ'] = df_charging_stations['PLZ'].astype(int)
    logger.debug(f"Converted PLZ column to int in charging stations DataFrame. Shape: {df_charging_stations.shape}")
    df_charging_stations = df_charging_stations.iloc[:, 0:2]
    df_merged = df_population.merge(df_charging_stations, on='PLZ', how='left')
    logger.info(f"Merged population and charging stations DataFrames. Shape: {df_merged.shape}")
    logger.debug(f"First 5 rows of the merged DataFrame:\n{df_merged.head(5)}")

    # Fill NaN values with 0
    df_merged['Number'] = df_merged['Number'].fillna(0)
    logger.info("Filling NaN values in 'Number' column with 0.")

    logger.info("merge_geo_dataframes function completed successfully.")
    return df_merged


# -----------------------------------------------------------------------------
@lg.logger_decorator
def create_electric_charging_residents_heatmap(df_charging_stations, df_population):
    """
    Generates a Streamlit app for visualizing heatmaps of charging stations, residents, and demand.
    """
    # Constants for defaults
    DEFAULT_MAP_LOCATION = [52.52, 13.40]  # Berlin coordinates
    DEFAULT_MAP_WIDTH, DEFAULT_MAP_HEIGHT = 800, 600

    """Main application function."""
    st.title("Electric Charging Stations and Residents Heatmap")
    df_merged = merge(df_charging_stations, df_population, on='PLZ',)
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

        # Login section
    if not st.session_state.logged_in:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        st.stop()
    # Main application
    st.write(f"Welcome, {st.session_state.username}!")

    # Logout button
    if st.button("Logout", key="logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    # Search functionality
    search_plz = st.text_input("Search by Postal Code:")
    if st.button("Search", key="search"):
        try:
            result = SearchService.search_by_postal_code(
                df_merged,
                search_plz
            )
            logging.info(f"result shape: {result}\n")
            if result[0] ==[]:
                st.error("No results found.")
            else:
                st.info(f"Number of results found at Postal code {result[1].postal_code} are {result[1].stations_found}")
        except SearchException as e:
            st.error(str(e))

    # Layer selection and map
    layer_selection = st.radio(
        "Select Use Case to Map",
        ("Residents", "Charging_Stations", "Demand", "Rate")
    )

    folium_map = folium.Map(
        location=DEFAULT_MAP_LOCATION,
        zoom_start=10
    )
    # Handle layer selection
    if layer_selection == "Rate":
        with st.form("rating_form"):
            selected_station = st.text_input("Station ID or Name:")
            rating = st.slider("Rating (1-5):", 1, 5, 3)
            submit_rating = st.form_submit_button("Submit Rating")

            if submit_rating:
                conn = sqlite3.connect('heatmap_app.db')
                c = conn.cursor()
                c.execute(
                    "INSERT INTO station_ratings VALUES (?, ?, ?, ?)",
                    (selected_station, st.session_state.username, rating, datetime.now())
                )
                conn.commit()
                conn.close()
                st.success(f"Rating submitted for station {selected_station}")
    else:
        color_map = None

        if layer_selection == "Residents":
            color_map,folium_map = mapping_residents(df_population, folium_map)
        elif layer_selection == "Charging_Stations":
            color_map,folium_map = mapping_stations(df_charging_stations, folium_map)
        elif layer_selection == "Demand":
            df_charging_stations['Demand'] = (merge(df_charging_stations, df_population, on='PLZ',).apply
                (      lambda row: DemandCalculator.calculate_demand(
                       row['Einwohner'], 50, row['Number']
                ),
                axis=1
            ))
            color_map, folium_map = mapping_demand(
                df_charging_stations,
                folium_map,
                'Demand',
                ['yellow', 'red'],
                "PLZ: {PLZ}, Demand: {Demand:.2f}"
            )

        if color_map:
            color_map.add_to(folium_map)

    # Display map
    folium_static(folium_map, width=DEFAULT_MAP_WIDTH, height=DEFAULT_MAP_HEIGHT)

# Function renamed to a more Pythonic style
# @lg.logger_decorator
# def create_electric_charging_residents_heatmap(df_charging_stations, df_population):
#     """
#     Generates a Streamlit app for visualizing heatmaps of charging stations, residents, and demand.
#     """
#     # Constants for defaults
#     DEFAULT_MAP_LOCATION = [52.52, 13.40]  # Berlin coordinates
#     DEFAULT_MAP_WIDTH, DEFAULT_MAP_HEIGHT = 800, 600
#
#     """Main application function."""
#     st.title("Electric Charging Stations and Residents Heatmap")
#
#     # Initialize session state
#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False
#     if "username" not in st.session_state:
#         st.session_state.username = None
#
#     # Login section
#     if not st.session_state.logged_in:
#         with st.form("login_form"):
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             submit = st.form_submit_button("Login")
#
#             if submit:
#                 if verify_user(username, password):
#                     st.session_state.logged_in = True
#                     st.session_state.username = username
#                     st.success("Login successful!")
#                     st.experimental_rerun()
#                 else:
#                     st.error("Invalid username or password")
#         st.stop()
#     def initialize_session():
#         """Initializes session states for login."""
#         if "logged_in" not in st.session_state:
#             st.session_state.logged_in = False
#
#     def login_section():
#         """Handles user login logic."""
#         if st.button("Click here to Login", key="button1"):
#             try:
#                 if handle_login():
#                     st.success("Login successful!")
#             except LoginException:
#                 st.error("Login failed. Please try again.")
#                 st.session_state.logged_in = False
#                 st.stop()
#         elif not st.session_state.logged_in:
#             st.info("Please login to continue.")
#             st.stop()
#
#     def search_by_postal_code(df):
#         """Adds postal code search functionality."""
#         search_plz = st.text_input("Search by Postal Code:")
#         if st.button("Search", key="button3"):
#             SearchService.search_by_postal_code(df, search_plz)
#
#     def add_folium_layer(selection, map_obj):
#         """Adds the selected layer to the Folium map."""
#         if selection == "Rate":
#             selected_station = st.text_input("Station ID or Name to Rate:")
#             rating = st.slider("Rate the Charging Station (1-5):", 1, 5, 3)
#             if st.button("Submit Rating", key="button4"):
#                 st.success(f"Thank you for rating Station {selected_station} with a {rating}!")
#         elif selection == "Residents":
#             return mapping_residents(df_population, map_obj)
#         elif selection == "Charging_Stations":
#             return mapping_stations(df_charging_stations, map_obj)
#         elif selection == "Demand":
#             # Adding demand calculation to the dataframe
#             df_charging_stations['Demand'] = df_charging_stations.apply(
#                 lambda row: demand_calculate.calculate_demand(row['Einwohner'], 50, row['Number']), axis=1
#             )
#             return mapping_demand(
#                 df_charging_stations,
#                 map_obj,
#                 column='Demand',
#                 colors=['yellow', 'red'],
#                 tooltip_template="PLZ: {PLZ}, Demand: {Demand:.2f}"
#             )
#     #--------------------------------------------------------------------
#     # Main app logic
#     st.title("Heatmaps: Electric Charging Stations and Residents")
#     initialize_session()
#     login_section()
#
#     if st.session_state.logged_in and st.button("Proceed", key="button2"):
#         search_by_postal_code(merge_geo_dataframes(df_charging_stations, df_population))
#
#     # Heatmap section
#     layer_selection = st.radio("Select Layer", ("Residents", "Charging_Stations", "Demand", "Rate"))
#     folium_map = folium.Map(location=DEFAULT_MAP_LOCATION, zoom_start=10)
#     color_map = add_folium_layer(layer_selection, folium_map)
#
#     if color_map:
#         color_map.add_to(folium_map)
#
#     folium_static(folium_map, width=DEFAULT_MAP_WIDTH, height=DEFAULT_MAP_HEIGHT)
