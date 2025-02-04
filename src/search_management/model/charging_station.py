from dataclasses import dataclass
from src.search_management.value_objects.postal_code import PostalCode
from src.search_management.value_objects.longitude import Longitude
from src.search_management.value_objects.latitude import Latitude
@dataclass
class ChargingStation:
    """
    Represents a charging station with location information.
    """
    postal_code: PostalCode
    latitude: Longitude
    longitude: Latitude

    def __post_init__(self):
        # Example logic to ensure attributes are correctly set or converted
        if not isinstance(self.postal_code, PostalCode):
            self.postal_code = PostalCode(self.postal_code)
        if not isinstance(self.latitude, Latitude):
            self.latitude = Latitude(self.latitude)
        if not isinstance(self.longitude, Longitude):
            self.longitude = Longitude(self.longitude)



