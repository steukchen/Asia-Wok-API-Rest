from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from app.core.config import settings
from functools import wraps
from typing import Callable

engine = create_engine(settings.DATABASE_URL,connect_args={"options": "-c timezone=utc"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def session(func: Callable):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        
        # Si se le pasa la session
        if(kwargs.get("session")):
            result = func(self, *args, **kwargs) 
            return result
        
        with SessionLocal() as session:
            try:
                kwargs['session'] = session
                result = func(self, *args, **kwargs) 
                return result
            except Exception:  
                session.rollback()  
                raise 
    
    return wrapper
