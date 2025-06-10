from sqlalchemy import Column,VARCHAR,NUMERIC
from .base import BaseID

class Currency(BaseID):
    __tablename__ = "currencies"
    name = Column(VARCHAR(255),nullable=False)
    exchange = Column(NUMERIC(10,4),nullable=False)