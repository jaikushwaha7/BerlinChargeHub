from narwhals import DataFrame

import src.utils.logger as lg


@lg.logger_decorator
# Add demand calculation function
class DemandCalculator:
    """
    Represents a demand calculation utility to estimate resource demand based on
    population, usage rate, and the number of available stations.

    This class provides methods to calculate the demand using specific parameters
    and to retrieve the formula used for calculation in LaTeX format.

    """

    def calculate_demand(population, usage_rate, number_of_stations):
        if population <= 0:
            raise ValueError("Population must be a positive value.")
        if usage_rate <= 0:
            raise ValueError("Usage rate must be a positive value.")
        if number_of_stations < 1:
            raise ValueError("Number of stations must be at least 1.")

        demand = (population * usage_rate / 100) / number_of_stations

        return demand

    def demand_formula_latex(self=None) -> object:
        return r"\frac{{\text{{population}} \cdot \text{{usage\_rate}}}}{{100 \cdot \text{{number\_of\_stations}}}}"

    def __str__(self):
        return self.demand_formula_latex()
