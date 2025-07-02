from sqlalchemy import VARCHAR,NUMERIC
from sqlalchemy.orm import mapped_column,Mapped
from .base import BaseID

class Currency(BaseID):
    __tablename__ = "currencies"
    name: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)
    exchange: Mapped[float] = mapped_column(NUMERIC(10,4),nullable=False)