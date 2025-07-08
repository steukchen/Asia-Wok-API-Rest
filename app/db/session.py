from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.exc import IntegrityError
from fastapi import status,HTTPException
from functools import wraps
from typing import Callable
from .exception import ExceptionRepository

engine = create_engine(settings.DATABASE_URL,connect_args={"options": "-c timezone=utc"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def session(func: Callable):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        
        # Si se le pasa la session
        external_session = kwargs.get("session")
        if external_session:
            return func(self, *args, **kwargs)
        
        with SessionLocal() as session:
            try:
                kwargs['session'] = session
                result = func(self, *args, **kwargs) 
                session.flush()
                if result is not None:
                    session.expunge_all()
                session.commit()
                return result
            except IntegrityError as e:
                error = str(e.orig).split("\n")[1]
                session.rollback()  
                
                if "ForeignKeyViolation" in str(e):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Foreign key violation: {error}")
                
                if "UniqueViolation" in str(e):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Unique violation: {error}")
                print(e)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Integrity Error: "+str(error))
            except ExceptionRepository as e:
                session.rollback()  
                raise HTTPException(status_code=e.code,detail=e.message)
            except Exception as e:  
                session.rollback()  
                print(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Exception: "+str(e))
    
    return wrapper

