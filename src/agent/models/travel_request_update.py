from typing import Optional
from pydantic import BaseModel


class TravelRequestUpdate(BaseModel):
    departure: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[int] = None
    travelers: Optional[int] = None
    budget: Optional[float] = None
    preferences: Optional[list[str]] = None
    service_requirements: Optional[list[str]] = None