
from sqlalchemy import  String,BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from agent.database.models.base import Base

class TravelStateModel(Base):
   __tablename__ = "travel_state"

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
   state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )