from sqlalchemy import Column,VARCHAR,TEXT
from .base import BaseID

class Customer(BaseID):
    __tablename__ = "customers"
    ci = Column(VARCHAR(255),nullable=False)
    name = Column(VARCHAR(255),nullable=False)
    lastname = Column(VARCHAR(255),nullable=False)
    phone_number = Column(VARCHAR(255))
    address = Column(TEXT)
    