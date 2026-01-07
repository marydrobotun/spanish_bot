from sqlalchemy import BigInteger, String, DateTime, func

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from settings import DEFAULT_LANGUAGE

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    language: Mapped[str] = mapped_column(String(5), default=DEFAULT_LANGUAGE, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
