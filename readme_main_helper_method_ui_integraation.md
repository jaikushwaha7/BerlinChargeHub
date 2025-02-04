+-----------------------------+      +--------------------------+ 
|         main.py             |      |      UI.py              |
| - Load datasets             |      | - Streamlit rendering   |
| - Preprocess datasets       |----->| - Heatmap visualization |
| - Merge GeoDataFrames       |      | - User authentication   |
| - Launch Streamlit          |      | - Search & demand       |
+-----------------------------+      +--------------------------+
                  |
      ------------------------------------
      |                                  |
+--------------------------+   +--------------------------------+
|      methods.py          |   |      HelperTools.py            |
| - Data cleaning          |   | - Utility functions           |
| - GeoDataFrame generation|   | - Serialization (pickle)      |
| - Station/Resident merge |   | - Column cleaning             |
+--------------------------+   +--------------------------------+
                  |
      +----------------------------------+
      |    Demand & Search Services      |
      | - DemandCalculator               |
      | - ChargingStationRating          |
      | - SearchService                  |
      +----------------------------------+
                     |
          +--------------------------------+
          |         Visualization Layer    |
          | - Folium Map Layers            |
          | - Residents (Population)       |
          | - Stations (Density)           |
          | - Demand (Scoring Formula)     |
          +--------------------------------+