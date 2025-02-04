                                                ┌───────────────────────────────────────────┐
                                                │               UI Layer                    │
                                                │  (Handle interaction between users &      │
                                                │       domain services/bounded contexts)   │
                                                └───────────────────────────────────────────┘
                                                                      │
                          ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
                          │                                                                                                                │
          ┌──────────────────────────────┐                                                                       ┌──────────────────────────────┐
          │        SearchContext         │                                                                       │         RatingContext        │
          │ (Handles search functionality│                                                                       │ (Handles station-specific    │
          │  for charging stations by    │                                                                       │   rating processes)          │
          │   using postal code)         │                                                                       │                              │
          └──────────────────────────────┘                                                                       └──────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│                        DOMAIN MODEL                          │
│       Core Business Logic, Entities, Value Objects           │
│                                                              │
│    ┌───────────────┐      ┌───────────────┐     ┌──────────┐ │
│    │ SearchContext │      │ RatingContext │     │ DemandCtx │ │
│    │───────────────│      │───────────────│     │──────────│ │
│    │               │      │               │     │          │ │
│    │ + SearchService│     │ + ChargeStation│    │ + Demand  │ │
│    │               │      │   Rating      │     │   Calc    │ │
│    │               │      │ + CleanSErr   │     │ Metrics   │ │
                                                                │
└──────────────────────────────────────────────────────────────┐


┌──────────────────────────────┐
│      Search Context          │
│ ┌──────────────────────────┐ │
│ |          Entities        | │
│ |  - ChargingStation       | │
│ |  - PostalCode            | │
│ └──────────────────────────┘ │
│ ┌──────────────────────────┐ │
│ |         Services         | │
│ |  - SearchService         | │
│ └──────────────────────────┘ │
│ ┌──────────────────────────┐ │
│ |         Events           | │
│ |  - StationSearchPerformed| │
│ └──────────────────────────┘ │
└──────────────────────────────┘
                                      +------------------------+
                                      |       User Action      |
                                      |  (e.g., search, rate)  |
                                      +------------------------+
                                                 |
                                                 v
+-------------------------+                                              +-------------------------+
|     Search Context      |                                              |     Rating Context      |
|                         |                                              |                         |
|      + Domain Event     |                                              |      + Domain Event     |
|      |                  |                                              |      |                  |
|      |StationSearchPerf.|                                              |      |RatingSubmitted    |
|      +------------------+                                              |      |RatingAvgCalculated|
|      + Entity           |                                              |      +------------------+
|      | ChargingStation  |                                              |      + Entity           |
|      +------------------+      +---------------------------------+     |      |       Rating      |
|      + Repository       |      |              Search             |     |      +------------------+
|      | GeoDataFrame     | ---> |   Fetch Charging Stations       |     |      + Repository       |
|      | Merge Datasets   |      |  by Postal Code or Location     |     |      |    RatingsRepo    |
|      +------------------+      +---------------------------------+     |      +------------------+
|                         |                                              |                         |
+-------------------------+                                              +-------------------------+
                                                 |
                                                 v
                                   +----------------------------+
                                   |     Demand Context         |
                                   |                            |
                                   |      + Domain Event        |
                                   |      | DemandScoreCalculated|
                                   |      +---------------------+
                                   |      + Value Objects       |
                                   |      | PostalCodePopulation|
                                   |      | DemandScore         |
                                   |      +---------------------+
                                   |      + Repository          |
                                   |      | Preprop LStat       |
                                   |      | Num of Stations     |
                                   |      +---------------------+
                                   +----------------------------+
                                                 |
                                                 v
                                      Demand Gets Calculated
                                                |
                                                v
                                      Domain Event Triggered
                                                |
                                                v
                               Event Log Captures Results for Use
