import pytest
from src.application.demand_calculator import demand_calculate


class TestDemandCalculate:
    def test_calculate_demand_valid_input(self):
        result = demand_calculate.calculate_demand(population=1000, usage_rate=50, number_of_stations=2)
        assert result == 250.0

    def test_calculate_demand_population_zero(self):
        with pytest.raises(ValueError, match="Population must be a positive value."):
            demand_calculate.calculate_demand(population=0, usage_rate=50, number_of_stations=2)

    def test_calculate_demand_population_negative(self):
        with pytest.raises(ValueError, match="Population must be a positive value."):
            demand_calculate.calculate_demand(population=-100, usage_rate=50, number_of_stations=2)

    def test_calculate_demand_usage_rate_zero(self):
        with pytest.raises(ValueError, match="Usage rate must be a positive value."):
            demand_calculate.calculate_demand(population=1000, usage_rate=0, number_of_stations=2)

    def test_calculate_demand_usage_rate_negative(self):
        with pytest.raises(ValueError, match="Usage rate must be a positive value."):
            demand_calculate.calculate_demand(population=1000, usage_rate=-10, number_of_stations=2)

    def test_calculate_demand_stations_zero(self):
        with pytest.raises(ValueError, match="Number of stations must be at least 1."):
            demand_calculate.calculate_demand(population=1000, usage_rate=50, number_of_stations=0)

    def test_calculate_demand_stations_negative(self):
        with pytest.raises(ValueError, match="Number of stations must be at least 1."):
            demand_calculate.calculate_demand(population=1000, usage_rate=50, number_of_stations=-5)

    def test_demand_formula_latex(self):
        result = demand_calculate.demand_formula_latex(None)
        expected = r"\frac{{\text{{population}} \cdot \text{{usage\_rate}}}}{{100 \cdot \text{{number\_of\_stations}}}}"
        assert result == expected
