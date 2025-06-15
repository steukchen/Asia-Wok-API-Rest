from .base import BaseID
from sqlalchemy import Column,VARCHAR

class DishType(BaseID):
    __tablename__ = "dishes_types"
    name = Column(VARCHAR(255),nullable=False)
    
