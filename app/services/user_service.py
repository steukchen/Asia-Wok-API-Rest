from app.db.repositories import UserRepository
from app.schemas.user import UserResponse
from typing import Dict
from .base_service import BaseService
from app.utils import validate_password

class UserService(BaseService):
    def __init__(self):
        self.repo = UserRepository()
        self.response = UserResponse
        
    def validate_user(self,username: str, password: str) -> Dict[str,str]:
        user_db = self.repo.get_one_by_column(column="username",value=username)
        if not user_db:
            return None
        if not user_db.status:
            return None
        
        if validate_password(hash=user_db.password,password=password):
            return {
                "id": str(user_db.id),
                "rol": str(user_db.rol)
            }
        return None

    def get_one_by_column_primary(self, value: str) -> UserResponse | None:
        item_db = self.repo.get_one_by_column_primary(value=value)
        if not item_db:
            return None
        if not item_db.status:
            return None
        
        return self._to_base_model(item_db=item_db)