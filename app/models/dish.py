from .base import BaseID
from sqlalchemy import VARCHAR,TEXT,NUMERIC,INTEGER,ForeignKey
from sqlalchemy.orm import mapped_column,Mapped

class Dish(BaseID):
    __tablename__ = "dishes"
    name: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)
    description: Mapped[str] = mapped_column(TEXT,nullable=False)
    price: Mapped[float] = mapped_column(NUMERIC(10,2),nullable=False)
    type_id: Mapped[int] = mapped_column(INTEGER,ForeignKey('dishes_types.id'),nullable=False)
    