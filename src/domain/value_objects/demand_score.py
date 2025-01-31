from dataclasses import dataclass
from src.exceptions.exceptions import InvalidDemandScoreException


@dataclass(frozen=True)
class DemandScore:
    """
    Represents the demand score with a value between 0 and 100.
    """
    score: float
    def __post_init__(self):
        if self.score < 0 or self.score > 100:
            raise InvalidDemandScoreException("Score must be between 0 and 100")