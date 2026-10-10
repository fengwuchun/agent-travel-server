from agent.database.models.base import Base
from sqlalchemy import BigInteger, String, Text,DateTime,func,Integer,Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime





class TravelRequestModel(Base):
    __tablename__ = "travel_request"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    thread_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
        
    )

    departure: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    destination: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    start_date: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    end_date: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    duration: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    travelers: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    budget: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    preferences: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    service_requirements: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

