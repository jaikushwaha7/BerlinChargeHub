+-----------------------+
|   DemandCalculator    |
+-----------------------+
| + calculate_demand()  |
| + demand_formula_latex|
| + __str__()           |
+-----------------------+
              ^
              |
              |
+-------------------------------+
| PostalCodePopulation          |
+-------------------------------+
| + value()                     |
| [Encapsulates population data]|
+-------------------------------+

+-------------------------------+
| NumberOfChargingStation       |
+-------------------------------+
| + number                      |
| [Encapsulates station number] |
+-------------------------------+

+--------------------------------+
| DemandScoreCalculated          |
+--------------------------------+
| + postal_code                  |
| + demand_score                 |
| [Result of demand calculation] |
+--------------------------------+


+-----------------------------+
| APPLICATION LAYER           |
|-----------------------------|
| DemandCalculator (Service)  |
| - Orchestrates demand logic |
| + calculate_demand()        |
|-----------------------------|
| [Depends on Domain Layer]   |
+-----------------------------+
             |
             |
+---------------------------------------+
| DOMAIN LAYER: Demand Management       |
|---------------------------------------|
| Aggregates:                           |
| - PostalCodePopulation +              |
|   NumberOfChargingStation             |
| Value Objects:                        |
| - PostalCodePopulation                |
| - NumberOfChargingStation             |
| Domain Entity:                        |
| - DemandScoreCalculated               |
|---------------------------------------|
| [Encapsulates business logic here]    |
+---------------------------------------+
             |
             |
+---------------------------------------------+
| INFRASTRUCTURE & EXTERNAL CONTEXTS          |
|---------------------------------------------|
| Search Management:                          |
| - StationSearchPerformed                    |
| - Logger Decorator (Wraps behavior)         |
|---------------------------------------------|
| [Provides supporting infrastructure]        |
+---------------------------------------------+