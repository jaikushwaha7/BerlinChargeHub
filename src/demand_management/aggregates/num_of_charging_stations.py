from dataclasses import dataclass
from src.search_management.value_objects.postal_code import PostalCode

@dataclass
class NumberOfChargingStation:
    postal_code: PostalCode
    number: int

