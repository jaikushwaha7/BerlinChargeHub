
import folium
import streamlit as st
from pandas import merge
from streamlit_folium import folium_static

import src.pages.infrastructure.core.HelperTools as ht
from src.pages.infrastructure.core.methods import merge_geo_dataframes
from src.rating_management.application.charging_station_rate import ChargeStationRating
from src.search_management.application.charging_station_search import SearchService
from src.demand_management.application.demand_calculator import DemandCalculator
from src.visualization_helper.mapping import mapping_residents, mapping_stations, mapping_demand
from src.utils.exceptions import SearchException
from src.utils import logger as lg
from src.utils.database_utils import verify_user


# Constants
DEFAULT_MAP_LOCATION = [52.52, 13.40]  # Berlin coordinates
DEFAULT_MAP_WIDTH = 800
DEFAULT_MAP_HEIGHT = 600


@lg.logger_decorator
def create_electric_charging_residents_heatmap(df_charging_stations, df_population, df_lstat2):
    """
    Generates an interactive heatmap application for electric charging stations
    and residential density, incorporating user authentication, search functionality,
    and map rendering features.
    """

    def initialize_session_state():
        """Initialize session state for user authentication."""
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "username" not in st.session_state:
            st.session_state.username = None

    def handle_login():
        """Display login form and handle user authentication."""
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Please enter valid username or password")
        st.stop()

    def display_logout_button():
        """Display logout button."""
        if st.button("Logout", key="logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    def handle_search(df_merged):
        """Handle postal code-based search and display results."""
        search_plz = st.text_input("Search by Postal Code:")
        if st.button("Search", key="search"):
            try:
                search = SearchService()
                result = search.search_by_postal_code(df_merged, search_plz)
                if result and len(result) > 0 and result[0]:
                    st.info(
                        f"Number of Charging Stations found at Postal Code {result[1].postal_code} -> "
                        f"{result[1].stations_found}")
                else:
                    st.error("No results found.")
            except SearchException as e:
                st.error(str(e))

    def render_map_layers(layer_selection, folium_map, df_merged):
        """Render layers based on user selection."""
        if layer_selection == "Rate":
            ChargeStationRating().charge_station_rating(df_lstat2, df_merged)
        elif layer_selection == "Residents":
            color_map, folium_map = mapping_residents(df_population, folium_map)
        elif layer_selection == "Charging Stations":
            color_map, folium_map = mapping_stations(df_charging_stations, folium_map)
        elif layer_selection == "Demand":
            display_demand_info(folium_map, df_charging_stations, df_population)
        return folium_map

    def display_demand_info(folium_map, df_charging_stations, df_population):
        """Calculate and map demand scores for postal codes."""
        st.info("Demand Score formula")
        st.latex(DemandCalculator().demand_formula_latex())
        df_charging_stations['Demand'] = merge(df_charging_stations, df_population, on='PLZ').apply(
            lambda row: DemandCalculator().calculate_demand(
                row['Einwohner'], 50, row['Number'], row['PLZ']
            ),
            axis=1
        )
        color_map, folium_map = mapping_demand(
            df_charging_stations,
            folium_map,
            'Demand',
            ['yellow', 'red'],
            "PLZ: {PLZ}, Demand: {Demand:.2f}"
        )
        color_map.add_to(folium_map)

    # Initialize the user interface
    st.title("Electric Charging Stations and Residents Heatmap")
    initialize_session_state()
    df_merged = merge_geo_dataframes(df_charging_stations, df_population)

    # User authentication
    if not st.session_state.logged_in:
        handle_login()
    st.write(f"Welcome, {st.session_state.username}!")
    display_logout_button()

    # Search functionality
    handle_search(df_merged)

    # Sidebar and map rendering
    st.sidebar.header("🚀 Service Options")
    layer_selection = st.sidebar.radio(
        "Select Use Case to Map or rate:",
        ("Residents", "Charging Stations", "Demand", "Rate")
    )
    folium_map = folium.Map(location=DEFAULT_MAP_LOCATION, zoom_start=10)
    render_map_layers(layer_selection, folium_map, df_merged)

    # Display the final map
    folium_static(folium_map, width=DEFAULT_MAP_WIDTH, height=DEFAULT_MAP_HEIGHT)
