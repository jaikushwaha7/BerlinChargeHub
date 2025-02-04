from dataclasses import dataclass
from src.utils.exceptions import InvalidPostalCodeException
@dataclass
class PostalCode:
    """
    Represents a postal code entity as a data class.
    """
    value: str

    def __post_init__(self):
        if not self.value.isdigit() or len(self.value) != 5:
            raise InvalidPostalCodeException("Postal code must be 5 digits")
