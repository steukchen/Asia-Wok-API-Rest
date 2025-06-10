from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from app.core.config import settings
from functools import wraps

engine = create_engine(settings.DATABASE_URL,connect_args={"options": "-c timezone=utc"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def session(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        with SessionLocal() as session:
            try:
                result = func(self, session, *args, **kwargs) 
                return result
            except Exception:  
                session.rollback()  
                raise 
    
    return wrapper
