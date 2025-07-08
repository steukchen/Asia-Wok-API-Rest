from app.models import User
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        self.base = User
        self.column_primary = "id"