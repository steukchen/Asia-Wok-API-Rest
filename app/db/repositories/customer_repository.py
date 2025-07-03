from .base_repository import BaseRepository
from ...models import Customer

class CustomerRepository(BaseRepository):
    def __init__(self):
        self.base = Customer