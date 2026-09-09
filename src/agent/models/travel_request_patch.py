from dataclasses import dataclass
@dataclass


class TravelRequestPatch:

    departure: str | None = None
    destination: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    duration: int | None = None
    travelers: int | None = None
    budget: float | None = None
    preferences: list[str] | None = None