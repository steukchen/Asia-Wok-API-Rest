from app.models import DishType
from .base_repository import BaseRepository

class DishTypeRepository(BaseRepository):
    def __init__(self):
        self.base = DishType
    