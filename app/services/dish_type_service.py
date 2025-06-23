from app.db.repositories import DishTypeRepository
from typing import List
from app.schemas.dish import DishTypeRequest,DishTypeResponse
from .base_service import BaseService

class DishTypeService(BaseService):
    def __init__(self):
        self.repo = DishTypeRepository()
        self.response = DishTypeResponse
    
    def get_dishes_types(self) -> List[DishTypeResponse]:
        dishes_types_db = self.repo.get_all()
        if not dishes_types_db:
            return None
        dishes_types_response = [DishTypeResponse(
            id=dish_type_db.id,
            name=dish_type_db.name,
        ) for dish_type_db in dishes_types_db]
        return dishes_types_response
    
    def create_dish_type(self,dish_type_request: DishTypeRequest) -> DishTypeResponse | None:
        dish_type = self.repo.create_one(data=dish_type_request)
        
        if not dish_type:
            return None
        
        return DishTypeResponse(
            id=dish_type.id,
            name=dish_type.name
        )
    
    def update_dish_type(self,dish_type_update: DishTypeRequest, id: int):
        dish_type = self.repo.update_one_by_column_primary(data=dish_type_update,value=id)
        
        if not dish_type:
            return None
        
        return DishTypeResponse(
            id=dish_type.id,
            name=dish_type.name
        )
        
    def delete_dish_type(self,id: int) -> bool:
        
        dish_type_deleted = self.repo.delete_one_by_column_primary(value=id)
        
        if not dish_type_deleted:
            return False
        
        return True
