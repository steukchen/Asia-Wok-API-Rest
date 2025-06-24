from app.db.repositories import UserRepository
from app.schemas.user import UserResponse,UserRequest,UserUpdate
from typing import List
from .base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        self.repo = UserRepository()
        self.response = UserResponse

    def create_user(self,user_request: UserRequest) -> UserResponse | None:
        user = self.repo.create_one(data=user_request)
        
        if user:
            return UserResponse(
                id=str(user.id),
                username=user.username,
                email=user.email,
                rol=user.rol
            )
        return None
    
    def update_user(self,user_update: UserUpdate, username: str):
        username = username.upper()
        user = self.repo.update_one_by_column_primary(data=user_update,value=username)
        
        
        if not user:
            return None
        
        user.id = str(user.id)
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            rol=user.rol
        )
        
    def delete_user(self,username: str) -> bool:
        username = username.upper()
        
        is_user_deleted = self.repo.delete_one_by_column_primary(value=username)
        
        return is_user_deleted
