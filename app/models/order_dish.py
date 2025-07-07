from sqlalchemy import INTEGER, ForeignKey,NUMERIC
from sqlalchemy.orm import mapped_column, Mapped
from .base import BaseID

class OrderDish(BaseID):
    __tablename__ = "order_dishes"
    order_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("orders.id"),nullable=False)
    dish_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("dishes.id"),nullable=False)
    quantity: Mapped[int] = mapped_column(INTEGER,nullable=False)
    price: Mapped[float] = mapped_column(NUMERIC(10,2),nullable=False)