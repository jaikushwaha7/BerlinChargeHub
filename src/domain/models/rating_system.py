from dataclasses import dataclass
from typing import Optional

@dataclass
class Rating:
    id: str
    user_id: str
    station_id: str
    stars: int
    review: Optional[str]
