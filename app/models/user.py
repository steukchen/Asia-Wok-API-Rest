from sqlalchemy import UUID,VARCHAR,Column,text
from .base import Base,roles

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID,primary_key=True,server_default=text('gen_random_uuid()'))
    username = Column(VARCHAR(255),nullable=False)
    email = Column(VARCHAR(255),nullable=False)
    rol = Column(roles,nullable=False)
    password = Column(VARCHAR(255),nullable=False)