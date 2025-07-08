from sqlalchemy import INTEGER,NUMERIC,ForeignKey
from sqlalchemy.orm import mapped_column,Mapped
from .base import BaseID

class OrderCurrency(BaseID):
    __tablename__ = "order_currencies"
    order_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("orders.id"),nullable=False)
    currency_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("currencies.id"),nullable=False)
    quantity: Mapped[float] = mapped_column(NUMERIC(10,2),nullable=False)
    exchange: Mapped[float] = mapped_column(NUMERIC(10,2),nullable=False)
    