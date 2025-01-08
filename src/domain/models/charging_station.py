from dataclasses import dataclass


@dataclass
class ChargingStation:
    """
    Represents a charging station with location information.
    """
    postal_code: str
    latitude: float
    longitude: float

    def is_in_postal_code(self, postal_code: str) -> bool:
        return self.postal_code == postal_code

@dataclass
class Location:
    """
    Represents a geographical location using latitude and longitude coordinates.
    """
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"