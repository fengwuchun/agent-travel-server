from agent.database.models.base import Base
from sqlalchemy import BigInteger, String, Text,DateTime,func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
class MessageModel(Base):
   __tablename__ = "message"
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

   role: Mapped[str] = mapped_column(
      String(100),
      nullable=False
   )

   content: Mapped[str] = mapped_column(
      Text,
      nullable=False
   )

   created_at: Mapped[datetime] = mapped_column(
      DateTime,
      default=func.now(),
      nullable=False
   )

   state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

   
