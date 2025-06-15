from sqlalchemy.dialects.postgresql import JSONB,UUID,TIMESTAMP,INTEGER
from sqlalchemy import Column,ForeignKey,text
from .base import DeclarativeBase,actions

class OrderCurrencyAudit(DeclarativeBase):
    __tablename__ = "order_currencies_audit"
    id =  Column(INTEGER,primary_key=True,autoincrement=True)
    order_id = Column(INTEGER,ForeignKey("orders.id"))
    action = Column(actions,nullable=False)
    old_data = Column(JSONB,nullable=False)
    new_data = Column(JSONB,nullable=False)
    changed_by = Column(UUID,ForeignKey("users.id"),nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))