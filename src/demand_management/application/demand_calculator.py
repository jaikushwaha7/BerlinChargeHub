
from src.search_management.events.station_search_performed import StationSearchPerformed
import src.utils.logger as lg

from src.demand_management.events.demand_score_calculated import DemandScoreCalculated
from src.demand_management.value_objects.postal_code_population import PostalCodePopulation
from src.demand_management.aggregates.num_of_charging_stations import  NumberOfChargingStation
@lg.logger_decorator
# Add demand calculation function
class DemandCalculator:
    """
    Represents a demand calculation utility to estimate resource demand based on
    population, usage rate, and the number of available stations.

    This class provides methods to calculate the demand using specific parameters
    and to retrieve the formula used for calculation in LaTeX format.

    """

    @staticmethod
    def calculate_demand(population: PostalCodePopulation, usage_rate: float, number_of_stations: NumberOfChargingStation,
                         postal_code: str):
        #  validate input values
        if isinstance(population, PostalCodePopulation):
            population_value = population.value()
        elif isinstance(population, int):
            population_value = population  # Use the raw integer
        else:
            raise TypeError("Population must be an int or PostalCodePopulation object.")

        # Validate number_of_stations input
        if isinstance(number_of_stations, NumberOfChargingStation):
            number_of_stations_value = number_of_stations.number
        elif isinstance(number_of_stations, int):  # Allow plain integer
            number_of_stations_value = number_of_stations
        else:
            raise TypeError("number_of_stations must be an int or NumberOfChargingStation instance.")

        # Validate input values
        if number_of_stations < 1:
            raise ValueError("Number of stations must be at least 1.")


        if population_value <= 0:
            raise ValueError("Population must be a positive value.")
        if usage_rate <= 0:
            raise ValueError("Usage rate must be a positive value.")
        if number_of_stations < 1:
            raise ValueError("Number of stations must be at least 1.")

        # Perform Calculation
        demand_score = (population_value * usage_rate / 100) / number_of_stations
        demand = DemandScoreCalculated(
            postal_code=postal_code,
            demand_score= demand_score
        )

        return demand_score

# class BasicFormulaProvider(FormulaProvider):
#     def demand_formula_latex(self) -> str:
#         return r"Demand Score: \frac{{\text{{population}} \cdot \text{{usage\_rate}}}}{{100 \cdot \text{{number\_of\_stations}}}}"
    def demand_formula_latex(self) -> str:
        return r"Demand  Score: \frac{{\text{{population}} \cdot \text{{usage\_rate}}}}{{100 \cdot \text{{number\_of\_stations}}}}"
    def __str__(self):
        return self.demand_formula_latex()

