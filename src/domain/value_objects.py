from dataclasses import dataclass

@dataclass(frozen=True)
class PostalCode:
    value: str

    def __post_init__(self):
        if not self.value.isdigit() or len(self.value) != 5:
            raise ValueError("Postal code must be 5 digits")

@dataclass(frozen=True)
class DemandScore:
    value: float

    def __post_init__(self):
        if not 0 <= self.value <= 100:
            raise ValueError("Demand score must be between 0 and 100")