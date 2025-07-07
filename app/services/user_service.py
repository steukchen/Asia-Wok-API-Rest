from app.db.repositories import UserRepository
from app.schemas.user import UserResponse,UserRequest,UserUpdate
from typing import List
from .base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        self.repo = UserRepository()
        self.response = UserResponse