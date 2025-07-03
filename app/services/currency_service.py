from .base_service import BaseService
from app.schemas.currency import CurrencyResponse
from app.db.repositories import CurrencyRepository

class CurrencyService(BaseService):
    def __init__(self):
        self.response = CurrencyResponse
        self.repo = CurrencyRepository()