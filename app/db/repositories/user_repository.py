from app.models import User
from app.schemas.user import UserRequest,UserUpdate
from sqlalchemy.orm import Session
from app.db import session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class UserRepository:
    
    @session
    def get_user_by_username(self,session: Session,username:str) -> User:
        try:
            query = select(User).where(User.username == username)
            user = session.execute(query).one()
            return user[0]
        except Exception as e:
            print(e)
        
        return None
    
    
    @session
    def create_user(self,session: Session, user_request: UserRequest) ->  User | None:
        user_db = User(
                username=user_request.username,
                email=user_request.email,
                rol=user_request.rol,
                password=user_request.password
            )

        try:
            session.add(user_db)
            session.commit()
            
            user = self.get_user_by_username(session=session,username=user_request.username)
            
            return user
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return None
    
    @session
    def update_user(self,session: Session, user_update: UserUpdate, username: str) -> User | None:
        user = self.get_user_by_username(session=session,username=username)
        
        if not user:
            return None
        
        user_update = user_update.model_dump()
        try:
            for property,value in user_update.items():
                if value is not None:
                    setattr(user,property,value)
            session.commit()
            session.flush()
            user = self.get_user_by_username(session=session,username=user.username)
            return user
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return None
    
    @session
    def delete_user(self,session: Session, username: str) -> bool:
        user = self.get_user_by_username(session=session,username=username)
        
        if not user:
            return False
        
        try:
            session.delete(user)
            session.commit()
            
            return True
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return False