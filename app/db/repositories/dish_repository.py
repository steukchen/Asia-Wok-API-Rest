from app.models import DishType
from app.schemas.dish import DishTypeRequest
from typing import List
from sqlalchemy.orm import Session
from app.db import session
from sqlalchemy import select

class DishRepository:
    
    @session
    def get_dishes_types(self,session: Session) -> List[DishType] | None:
        query = select(DishType)
        dishes_types = session.execute(query).all()
        if not dishes_types:
            return None
        dishes_types = [dish_type[0] for dish_type in dishes_types]
        return dishes_types
    
    @session
    def get_dish_type_by_id(self,session: Session,id:int) -> DishType | None:
        query = select(DishType).where(DishType.id == id)
        dish_type = session.execute(query).fetchone()
        if not dish_type:
            return None
        return dish_type[0]
    
    
    @session
    def create_dish_type(self,session: Session, dish_type_request: DishTypeRequest) ->  DishType:
        dish_type_db = DishType(
                name=dish_type_request.name,
            )
        session.add(dish_type_db)
        
        return dish_type_db
    
    @session
    def update_dish_type(self,session: Session, dish_type_update: DishTypeRequest, id: int) -> DishType | None:
        dish_type = self.get_dish_type_by_id(session=session,id=id)
        
        if not dish_type:
            return None
        
        dish_type_update = dish_type_update.model_dump()
        
        for property,value in dish_type_update.items():
            if value is not None:
                setattr(dish_type,property,value)
        return dish_type
    
    @session
    def delete_dish_type(self,session: Session, id: int) -> bool:
        dish_type = self.get_dish_type_by_id(session=session,id=id)
        
        if dish_type:
            session.delete(dish_type)
        
        return dish_type is not None