from app.db.repositories import CustomerRepository
from app.schemas.customer import CustomerResponse
from .base_service import BaseService

class CustomerService(BaseService):
    def __init__(self):
        self.repo = CustomerRepository()
        self.response = CustomerResponse
