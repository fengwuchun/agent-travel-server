from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from agent.database.models.base import Base
from datetime import datetime

class Conversation(Base):

    __tablename__ = "conversation"

    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    thread_id:Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )


    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False
    )

    
