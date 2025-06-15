from sqlalchemy import UUID,VARCHAR,text
from sqlalchemy.orm import mapped_column,Mapped
from .base import Base,roles

class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(UUID,primary_key=True,server_default=text('gen_random_uuid()'))
    username: Mapped[str] = mapped_column(VARCHAR(255),nullable=False,unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255),nullable=False,unique=True)
    rol: Mapped[str] = mapped_column(roles,nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(255),nullable=False)