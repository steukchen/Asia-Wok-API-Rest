from sqlalchemy import TIMESTAMP,INTEGER,UUID,ForeignKey,text,TEXT
from sqlalchemy.orm import mapped_column,Mapped
from .base import BaseID,order_states

class Order(BaseID):
    __tablename__ = "orders"
    customer_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("customers.id"),nullable=True)
    order_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))
    created_by: Mapped[UUID] = mapped_column(UUID,ForeignKey("users.id"),nullable=False)
    notes: Mapped[str] = mapped_column(TEXT,nullable=True)
    table_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("tables.id"),nullable=False)
    state: Mapped[str] = mapped_column(order_states,nullable=False,server_default=text("'pending'"))