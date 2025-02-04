from dataclasses import dataclass
from src.exceptions.exceptions import InvalidDemandScoreException


@dataclass(frozen=True)
class DemandScore:
    """
    Represents the demand score for a postal code.
    """
    score: float
    
    def __post_init__(self):
        if not isinstance(self.score, float):
            raise InvalidDemandScoreException(f"Invalid data type for demand score: {type(self.score).__name__}. Expected type: float.")
    