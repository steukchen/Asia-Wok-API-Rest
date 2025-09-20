from sqlalchemy.orm import declarative_base
from sqlalchemy import Enum,TIMESTAMP,text,INTEGER,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from app.db.session import engine,SessionLocal

DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True
    status: Mapped[bool] = mapped_column(Boolean,nullable=False,server_default=text("TRUE"))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))

class BaseID(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(INTEGER,primary_key=True,autoincrement=True)

roles = Enum('admin','cashier','chef','waiter',name="roles")
states_tables = Enum('enabled','disabled','occupied','reserved',name="states_tables")
actions = Enum('created','updated','deleted',name="actions")
order_states = Enum('pending','preparing','made','completed','cancelled',name="order_states")

async def create_structure():
    DeclarativeBase.metadata.create_all(bind=engine)
    with open("SQL/functions.sql","r") as file:
        sql = text(file.read())
    
    with SessionLocal() as session:
        session.execute(sql)
        session.commit()
    print("Database structure created")
    