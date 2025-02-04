from dataclasses import dataclass
from src.rating_management.value_objects.rating_average import RatingAverage
from src.rating_management.value_objects.address import Address
from src.search_management.value_objects.postal_code import PostalCode
@dataclass
class RatingAverageCalculated:

    rating_average: RatingAverage
    station_postal_code: PostalCode
    station_address: Address