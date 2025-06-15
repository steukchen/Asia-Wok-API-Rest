from sqlalchemy import VARCHAR,Column,text
from .base import BaseID,states_tables

class Table(BaseID):
    __tablename__ = "tables"
    name = Column(VARCHAR(255),nullable=False)
    state = Column(states_tables,nullable=False,server_default=text("'enabled'"))
    