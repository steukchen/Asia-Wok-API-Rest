from sqlalchemy import VARCHAR,TEXT
from sqlalchemy.orm import mapped_column,Mapped
from .base import BaseID

class Customer(BaseID):
    __tablename__ = "customers"
    ci: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)
    lastname: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255))
    address: Mapped[str] = mapped_column(TEXT)
    