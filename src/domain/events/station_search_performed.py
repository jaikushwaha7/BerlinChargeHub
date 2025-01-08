from dataclasses import dataclass
from datetime import datetime

@dataclass
class StationSearchPerformed:
    """
    Represents the result of a search operation for stations within a given postal code.

    This class is used to encapsulate the details of a station search operation, including
    when the search was performed, the postal code used in the search, and the number of
    stations that were found during the search.

    """
    timestamp: datetime
    postal_code: str
    stations_found: int