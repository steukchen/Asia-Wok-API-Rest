from app.models import User
from sqlalchemy.orm import Session
from app.db import session
from sqlalchemy import select

class UserRepository:
    
    @session
    def get_user_by_username(self,session: Session,username:str) -> User:
        try:
            query = select(User).where(User.username == username)
            user = session.execute(query).one_or_none()
            return user[0]
        except Exception as e:
            print(e)
        
        return None
            