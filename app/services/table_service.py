from app.db.repositories import TableRepository
from typing import List
from app.schemas.table import TableResponse,TableRequest,TableUpdate
from .base_service import BaseService

class TableService(BaseService):
    def __init__(self):
        self.repo = TableRepository()
        self.response = TableResponse