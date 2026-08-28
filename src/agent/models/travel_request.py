from dataclasses import dataclass
@dataclass

class TravelRequest:
        departure: str
        destination: str
        start_date: str
        end_date: str
        duration: int
        travelers: int
        budget: float
        preferences: list[str] 