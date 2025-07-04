from .base_repository import BaseRepository
from app.models import Customer

class CustomerRepository(BaseRepository):
    def __init__(self):
        self.base = Customer