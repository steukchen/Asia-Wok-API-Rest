from .base import BaseID
from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column,Mapped

class DishType(BaseID):
    __tablename__ = "dishes_types"
    name: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)
    
