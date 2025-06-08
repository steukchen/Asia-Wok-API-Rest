from .base import BaseID
from sqlalchemy import Column,VARCHAR,TEXT,NUMERIC,INTEGER,ForeignKey

class Dish(BaseID):
    __tablename__ = "dishes"
    name = Column(VARCHAR(255),nullable=False)
    description = Column(TEXT,nullable=False)
    price = Column(NUMERIC(10,2),nullable=False)
    type_id = Column(INTEGER,ForeignKey('dishes_types.id'),nullable=False)
    