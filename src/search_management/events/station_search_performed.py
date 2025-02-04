from dataclasses import dataclass
from datetime import datetime
from src.search_management.model.charging_station import ChargingStation
from src.search_management.value_objects.postal_code import PostalCode
@dataclass
class StationSearchPerformed:
    """
    Represents the result of a search operation for stations within a given postal code.

    This class is used to encapsulate the details of a station search operation, including
    when the search was performed, the postal code used in the search, and the number of
    stations that were found during the search.

    """
    timestamp: datetime
    postal_code: PostalCode
    stations_found: int