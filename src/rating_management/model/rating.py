from dataclasses import dataclass
from typing import Optional
from src.rating_management.value_objects.user import User
from src.rating_management.value_objects.stars import Stars
from src.rating_management.value_objects.address import Address
from src.search_management.value_objects.postal_code import PostalCode
@dataclass
class Rating:
    user_id: User
    station_address: Address
    stars: Stars
    station_postal_code: PostalCode
