import folium
from folium.plugins import HeatMap
import pandas as pd
import streamlit as st
from branca.colormap import LinearColormap
import src.utils.logger as lg
from src.utils.database_utils import verify_user

#
# def mapping_stations(df: pd.DataFrame, map_obj: folium.Map) -> folium.plugins.HeatMap:
#     """Create heatmap layer for charging stations."""
#     stations_data = df[['Latitude', 'Longitude', 'Number']].values.tolist()
#     return folium.plugins.HeatMap(
#         stations_data,
#         radius=15,
#         gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
#     )
#
#
# def mapping_residents(df: pd.DataFrame, map_obj: folium.Map) -> folium.plugins.HeatMap:
#     """Create heatmap layer for residents."""
#     residents_data = df[['Latitude', 'Longitude', 'Einwohner']].values.tolist()
#     return folium.plugins.HeatMap(
#         residents_data,
#         radius=15,
#         gradient={0.4: 'green', 0.65: 'yellow', 1: 'red'}
#     )
#
#
# def mapping_demand(
#         df: pd.DataFrame,
#         map_obj: folium.Map,
#         column: str,
#         colors: list,
#         tooltip_template: str
# ) -> folium.plugins.HeatMap:
#     """Create heatmap layer for demand."""
#     demand_data = df[['Latitude', 'Longitude', column]].values.tolist()
#     return folium.plugins.HeatMap(
#         demand_data,
#         radius=15,
#         gradient={0.4: colors[0], 1: colors[1]}
#     )
#


@lg.logger_decorator
def mapping_residents(df_population, folium_map):
    """
    Maps residents' population data onto a given Folium map using color gradients to represent
    the population information. The function applies a linear color mapping based on
    the range of population values and overlays the data onto geometries defined within
    the population DataFrame.

    """
    # Create a color map for Residents
    color_map = LinearColormap(colors=['#4C6CAF','#A5BAE6','#EAEF00', '#BEC123','#C98787', '#D60000'],
                               vmin=df_population['Einwohner'].min(),
                               vmax=df_population['Einwohner'].max())
    # Add polygons to the map for Residents
    for idx, row in df_population.iterrows():
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=color_map(row['Einwohner']): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
        ).add_to(folium_map)
    return color_map, folium_map

def mapping_stations(df_residents, folium_map):
    """
    For mapping Station data
    Map data points to a folium map with styled polygons and associated tooltips.

    This function takes a dataset of geographic regions with associated numerical
    data and a Folium map object, then visualizes the data by styling polygons
    on the map corresponding to the regions. The method also generates a linear
    color mapping based on the numerical values.


    """
    color_map = LinearColormap(colors=['#4C6CAF','#A5BAE6','#EAEF00', '#BEC123','#C98787', '#D60000'], vmin=df_residents['Number'].min(),
                               vmax=df_residents['Number'].max())
    # Add polygons to the map for Numbers
    for idx, row in df_residents.iterrows():
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=color_map(row['Number']): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}"
        ).add_to(folium_map)
    return color_map, folium_map

def mapping_demand(df, folium_map, column, colors, tooltip_template):
    """
    Maps demand on a geographical folium map based on data contained in the provided dataframe.
    This function iterates through each record in the dataframe, using the geometry information
    to create GeoJson objects that represent map features. These features are styled based on
    a color scale determined by the `colors` parameter and the specified column values. The
    function also uses a tooltip template to provide information about the mapped features when
    hovered over.


    """
    color_map = LinearColormap(colors=colors, vmin=df[column].min(), vmax=df[column].max())
    for _, record in df.iterrows():
        folium.GeoJson(
            record['geometry'],
            style_function=lambda x, color=color_map(record[column]): {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=tooltip_template.format(PLZ=record['PLZ'], Demand=record[column])
        ).add_to(folium_map)
    return color_map, folium_map