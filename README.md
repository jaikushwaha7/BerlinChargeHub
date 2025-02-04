```
<<<<<<< HEAD
project_root/
│
├── src/
│   ├── app/
│   │   ├── create_heatmap.py          # Main application script for Streamlit (Entry point for the app)
│   │
│   ├── infrastructure/
│   │   ├── core/
│   │   │   ├── HelperTools.py          # Contains helper functions (e.g., reusable tools like performance timing)
│   │   │   ├── methods.py              # Contains logical and reusable data processing methods like merging DataFrames
│   │
│   ├── search_management/
│   │   ├── application/
│   │   │   ├── charging_station_search.py  # Implements search functionality (e.g., SearchService class)
│   │   ├── domain/                      # Folder for domain-level abstractions (if needed for future growth)
│   │
│   ├── rating_management/
│   │   ├── application/
│   │   │   ├── charging_station_rate.py   # Manages station rating functionality (e.g., ChargeStationRating class)
│   │   ├── domain/                      # Folder for domain logic related to rating (optional)
│   │
│   ├── demand_management/
│   │   ├── application/
│   │   │   ├── demand_calculator.py      # Contains DemandCalculator for calculating demand and related formulas
│   │
│   ├── visualization_helper/
│   │   ├── mapping.py                   # Functions responsible for map-specific tasks (e.g., mapping_residents, mapping_stations)
│   │
│   ├── utils/
│   │   ├── logger.py                    # Logger utilities (e.g., @logger_decorator)
│   │   ├── exceptions.py                # Custom exception classes (e.g., SearchException)
│   │   ├── database_utils.py            # Utility functions for database-related tasks (e.g., verify_user function)
│
├── tests/
│   ├── test_create_heatmap.py           # Unit tests for the main heatmap app
│   ├── test_search_management.py        # Tests for SearchService-related methods
│   ├── test_rating_management.py        # Tests for charging station rating functionality
│   ├── test_demand_management.py        # Tests for demand calculation functionality
│   ├── test_visualization_helper.py     # Tests for map-rendering functions
│   ├── test_utils.py                    # Tests for utility functions (e.g., logger, database utilities, exceptions)
│
├── data/
│   ├── population_data.csv              # Example CSV file for population data
│   ├── charging_stations_data.csv       # Example CSV file for charging stations' data
│
├── requirements.txt                     # List of Python dependencies (e.g., streamlit, pandas, folium, etc.)
├── README.md                            # Project documentation
├── .gitignore                           # Git ignored files (e.g., *.pyc, __pycache__, local data files)
```

## Electric Charging Stations and Residents Heatmap
The **Electric Charging Stations and Residents Heatmap** is an interactive web application built with **Streamlit** and **Folium**. It provides a user-friendly interface to visualize electric vehicle charging station locations, residential density, and demand scores on an interactive map.
### Features
- **User Authentication**: Secure login and logout functionality for accessing the app.
- **Search by Postal Code**: Quickly find charging station information for specific postal codes.
- **Interactive Heatmaps**: Visualize various data layers, including:
    - Residential population density.
    - Electric charging station availability.
    - Demand scores for charging stations.
    - Charging station ratings.

- **Dynamic Demand Calculation**: Calculate demand scores using population, station count, and usage rates.
- **Customizable Map Layers**: Toggle between data layers dynamically for tailored insights.

### Use Cases
- **City Planners**: Identify areas with low charging station availability to guide resource allocation.
- **Business Analysts**: Evaluate the best locations to set up new charging stations.
- **EV Users**: Check charging station availability and ratings in your area.
