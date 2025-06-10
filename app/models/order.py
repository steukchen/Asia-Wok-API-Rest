from sqlalchemy import Column,TIMESTAMP,INTEGER,UUID,ForeignKey,text
from .base import BaseID,order_states

class Order(BaseID):
    __tablename__ = "orders"
    customer_id = Column(INTEGER,ForeignKey("customers.id"),nullable=False)
    order_date = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))
    created_by = Column(UUID,ForeignKey("users.id"),nullable=False)
    table_id = Column(INTEGER,ForeignKey("tables.id"),nullable=False)
    state = Column(order_states,nullable=False,server_default=text("'pending'"))