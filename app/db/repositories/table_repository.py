from app.models import Table
from .base_repository import BaseRepository

class TableRepository(BaseRepository):
    def __init__(self):
        self.base = Table