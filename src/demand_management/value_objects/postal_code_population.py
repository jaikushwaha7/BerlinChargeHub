from dataclasses import dataclass

@dataclass
class PostalCodePopulation:
    """
    Represents the population associated with a specific postal code.

    """
    def __init__(self, value: int):
        self._value = value

    def value(self):
        return self._value



