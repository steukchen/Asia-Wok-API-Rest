from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from app.core.config import settings
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.base import instance_state
from fastapi import status,HTTPException
from functools import wraps
from typing import Callable

engine = create_engine(settings.DATABASE_URL,connect_args={"options": "-c timezone=utc"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def is_sqlalchemy_instance(obj):
    try:
        instance_state(obj)
        return True
    except Exception:
        return False

def detach_sqlalchemy_objects(session: Session, result):
    if isinstance(result, list):
        for item in result:
            if is_sqlalchemy_instance(item):
                session.expunge(item)
    elif is_sqlalchemy_instance(result):
        session.expunge(result)
    return result

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
                result = detach_sqlalchemy_objects(session, result)
                session.commit()
                return result
            except IntegrityError as e:
                
                session.rollback()  
                
                if "ForeignKeyViolation" in str(e):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Foreign key violation")
                
                if "UniqueViolation" in str(e):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Unique violation")
                
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Integrity Error: "+str(e))
            except Exception as e:  
                session.rollback()  
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Exception: "+str(e))
    
    return wrapper
