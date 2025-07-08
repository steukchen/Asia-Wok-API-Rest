from .base_repository import BaseRepository
from app.models import Currency

class CurrencyRepository(BaseRepository):
    def __init__(self):
        self.base = Currency