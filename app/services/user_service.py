from app.db.repositories import UserRepository
from app.schemas.user import UserResponse,UserRequest,UserUpdate
from typing import Dict
from .base_service import BaseService
from app.utils import hash_password,validate_password

class UserService(BaseService):
    def __init__(self):
        self.repo = UserRepository()
        self.response = UserResponse
        
    def validate_user(self,username: str, password: str) -> Dict[str,str]:
        user_db = self.repo.get_one_by_column(column="username",value=username)
        if not user_db:
            return None
        
        if validate_password(hash=user_db.password,password=password):
            return {
                "id": str(user_db.id),
                "rol": str(user_db.rol)
            }
        return None