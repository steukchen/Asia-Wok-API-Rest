from sqlalchemy import Column, INTEGER,NUMERIC, ForeignKey
from .base import BaseID

class OrderCurrency(BaseID):
    __tablename__ = "order_currencies"
    order_id = Column(INTEGER,ForeignKey("orders.id"),nullable=False)
    currency_id = Column(INTEGER,ForeignKey("currencies.id"),nullable=False)
    quantity = Column(NUMERIC(10,2),nullable=False)
    