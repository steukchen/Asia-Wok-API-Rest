from sqlalchemy import VARCHAR,text
from sqlalchemy.orm import Mapped,mapped_column
from .base import BaseID,states_tables

class Table(BaseID):
    __tablename__ = "tables"
    name: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)
    state: Mapped[str] = mapped_column(states_tables,nullable=False,server_default=text("'enabled'"))
    