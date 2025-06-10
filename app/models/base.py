from sqlalchemy.orm import declarative_base
from sqlalchemy import Enum,TIMESTAMP,Column,text,INTEGER
from ..db.session import engine,SessionLocal

DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))

class BaseID(Base):
    __abstract__ = True
    id = Column(INTEGER,primary_key=True,autoincrement=True)

roles = Enum('superadmin','admin','chef','waiter',name="roles")
states_tables = Enum('enabled','disabled','occupied','reserved',name="states_tables")
actions = Enum('created','updated','deleted',name="actions")
order_states = Enum('pending','completed','cancelled',name="order_states")

async def create_structure():
    DeclarativeBase.metadata.create_all(bind=engine)
    with open("SQL/functions.sql","r") as file:
        sql = text(file.read())
    
    with SessionLocal() as session:
        session.execute(sql)
        session.commit()
    print("Database structure created")
    
def insert_data_test():
    with open("SQL/data_test.sql","r") as file:
        sql = text(file.read())
    with SessionLocal() as session:
        session.execute(sql)
        session.commit()