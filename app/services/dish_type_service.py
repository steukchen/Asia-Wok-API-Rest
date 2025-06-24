from app.db.repositories import DishTypeRepository
from app.schemas.dish import DishTypeResponse
from .base_service import BaseService

class DishTypeService(BaseService):
    def __init__(self):
        self.repo = DishTypeRepository()
        self.response = DishTypeResponse
