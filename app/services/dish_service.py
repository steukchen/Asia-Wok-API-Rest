from app.db.repositories import DishRepository
from app.schemas.dish import DishResponse,DishTypeResponse
from .base_service import BaseService
from typing import List

class DishService(BaseService):
    def __init__(self):
        self.repo = DishRepository()
        self.response = DishResponse
        
    def _to_base_models(self,items_db: list) -> List[DishResponse]:
        items_response = [DishResponse(
            id=item_db[0].id,
            name=item_db[0].name,
            description=item_db[0].description,
            price=item_db[0].price,
            type = DishTypeResponse(
                id=item_db[1].id,
                name=item_db[1].name
            )
        ) for item_db in items_db ]
        
        return items_response
    
    def _to_base_model(self,item_db: list) -> DishResponse:
        items_response = DishResponse(
            id=item_db[0].id,
            name=item_db[0].name,
            description=item_db[0].description,
            price=item_db[0].price,
            type = DishTypeResponse(
                id=item_db[1].id,
                name=item_db[1].name
            )
        )
        return items_response

    def get_all(self) -> List[DishResponse] | None:
        items_db = self.repo.get_dishes()
        
        if not items_db:
            return None
        return self._to_base_models(items_db=items_db)

    def get_dishes_by_name(self,name: str) -> List[DishResponse] | None:
        items_db = self.repo.get_dishes_by_name(name=name)
        
        if not items_db:
            return None
        
        return self._to_base_models(items_db=items_db)
    
    def get_dishes_by_type(self,type_id: int) -> List[DishResponse] | None:
        items_db = self.repo.get_dishes_by_type(type_id=type_id)
        
        if not items_db:
            return None
        
        return self._to_base_models(items_db=items_db)