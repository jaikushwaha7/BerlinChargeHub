import logging

import folium
import geopandas as gpd
import streamlit as st
from pandas import merge
from streamlit_folium import folium_static

import src.pages.infrastructure.core.HelperTools as ht
from src.rating_management.application.charging_station_rate import ChargeStationRating
from src.search_management.application.charging_station_search import SearchService
from src.demand_management.application.demand_calculator import DemandCalculator
from src.visualization_helper.mapping import mapping_residents, mapping_stations, mapping_demand
from src.utils.exceptions import SearchException
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
    
    logger.debug(f"Input DataFrame in preprop_resid shape: {dframe.shape}, Geo DataFrame shape: {df_geo.shape}")

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
    logger.debug(f"First 5 rows of the df_charging_stations DataFrame:\n{df_charging_stations.head(5)}")
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
