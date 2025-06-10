from sqlalchemy import Column, INTEGER, ForeignKey
from .base import BaseID

class OrderDish(BaseID):
    __tablename__ = "order_dishes"
    order_id = Column(INTEGER,ForeignKey("orders.id"),nullable=False)
    dish_id = Column(INTEGER,ForeignKey("dishes.id"),nullable=False)
    quantity = Column(INTEGER,nullable=False)
    