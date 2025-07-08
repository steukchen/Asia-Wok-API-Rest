from sqlalchemy.dialects.postgresql import JSONB,UUID,TIMESTAMP,INTEGER
from sqlalchemy import ForeignKey,text
from sqlalchemy.orm import mapped_column,Mapped
from .base import DeclarativeBase,actions

class OrderDishAudit(DeclarativeBase):
    __tablename__ = "order_dishes_audit"
    id: Mapped[int] =  mapped_column(INTEGER,primary_key=True,autoincrement=True)
    order_id: Mapped[int] = mapped_column(INTEGER,ForeignKey("orders.id"))
    action: Mapped[str] = mapped_column(actions,nullable=False)
    old_data: Mapped[dict] = mapped_column(JSONB,nullable=False)
    new_data: Mapped[dict] = mapped_column(JSONB,nullable=False)
    changed_by: Mapped[UUID] = mapped_column(UUID,ForeignKey("users.id"),nullable=False)
    changed_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))