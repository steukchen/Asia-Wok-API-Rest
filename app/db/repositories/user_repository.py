from app.models import User
from app.schemas.user import UserRequest,UserUpdate
from sqlalchemy.orm import Session
from app.db import session
from sqlalchemy import select
from typing import List

class UserRepository:
    
    @session
    def get_users(self,session: Session) -> List[User] | None:
        query = select(User)
        users = session.execute(query).all()
        if not users:
            return None
        users = [user[0] for user in users]
        return users
    @session
    def get_user_by_username(self,session: Session,username:str) -> User | None:
        query = select(User).where(User.username == username)
        user = session.execute(query).fetchone()
        if not user:
            return None
            
        return user[0]
        
    
    
    @session
    def create_user(self,session: Session, user_request: UserRequest) ->  User:
        user_db = User(
                username=user_request.username,
                email=user_request.email,
                rol=user_request.rol,
                password=user_request.password
            )
        
        session.add(user_db)
        return user_db
        
    
    @session
    def update_user(self,session: Session, user_update: UserUpdate, username: str) -> User | None:
        user = self.get_user_by_username(session=session,username=username)
        
        if not user:
            return None
        
        user_update = user_update.model_dump()
        
        for property,value in user_update.items():
            if value is not None:
                setattr(user,property,value)

        return user
        
    
    @session
    def delete_user(self,session: Session, username: str) -> bool:
        user = self.get_user_by_username(session=session,username=username)
        
        if user:
            session.delete(user)
        return user is not None