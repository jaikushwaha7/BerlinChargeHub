```
BerlinChargeHub/
├── .idea/
│   ├── workspace.xml
│   ├── modules.xml
│   └── ...
├── __pycache__/
│   └── ...
├── datasets/
│   ├── charging_stations.csv
│   ├── demand_data.csv
│   └── ...
├── presentation/
│   └── EventFlow_SequenceFlow/
│       ├── event_flow_diagram.png
│       ├── sequence_flow_chart.pdf
│       └── ...
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── events.py
│   │   └── exceptions.py
│   ├── application/
│   │   ├── __init__.py
│   │   └── services.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   └── repositories.py
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py
├── tests/
│   ├── __init__.py
│   ├── test_station_search.py
│   └── test_demand_indicator.py
├── README.md
├── config.py
├── .gitignore
├── main.py
└── requirements.txt

```

Notes:

.idea/: Contains IDE-specific settings and configurations.

datasets/: Includes data files such as charging_stations.csv and demand_data.csv.

presentation/EventFlow_SequenceFlow/: Houses presentation materials like event_flow_diagram.png and sequence_flow_chart.pdf.

src/: Main source code directory:

- domain/: Defines core domain logic with modules like models.py, events.py, and exceptions.py.
- application/: Contains application services, e.g., services.py.
- infrastructure/: Manages data access with repositories.py.
- utils/: Utility functions, including data_loader.py.

tests/: Contains test modules such as test_station_search.py and test_demand_indicator.py.

Root Files:

README.md: Project overview and documentation.
config.py: Configuration settings.
.gitignore: Specifies files and directories for Git to ignore.
main.py: Primary executable script.
requirements.txt: Lists project dependencies.