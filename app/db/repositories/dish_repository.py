from app.models import DishType
from app.schemas.dish import DishTypeRequest
from typing import List
from sqlalchemy.orm import Session
from app.db import session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class DishRepository:
    
    @session
    def get_dishes_types(self,session: Session) -> List[DishType]:
        try:
            query = select(DishType)
            dishes_types = session.execute(query).all()
            dishes_types = [dish_type[0] for dish_type in dishes_types]
            return dishes_types
        except Exception as e:
            print(e)
        
        return None
    
    @session
    def get_dish_type_by_id(self,session: Session,id:int) -> DishType:
        try:
            query = select(DishType).where(DishType.id == id)
            dish_type = session.execute(query).one()
            return dish_type[0]
        except Exception as e:
            print(e)
        
        return None
    
    
    @session
    def create_dish_type(self,session: Session, dish_type_request: DishTypeRequest) ->  DishType | None:
        dish_type_db = DishType(
                name=dish_type_request.name,
            )
        try:
            session.add(dish_type_db)
            session.commit()
            
            dish_type = self.get_dish_type_by_id(session=session,id=dish_type_db.id)
            
            return dish_type
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return None
    
    @session
    def update_dish_type(self,session: Session, dish_type_update: DishTypeRequest, id: int) -> DishType | None:
        dish_type = self.get_dish_type_by_id(session=session,id=id)
        
        if not dish_type:
            return None
        
        dish_type_update = dish_type_update.model_dump()
        try:
            for property,value in dish_type_update.items():
                if value is not None:
                    setattr(dish_type,property,value)
            session.commit()
            session.flush()
            dish_type = self.get_dish_type_by_id(session=session,id=dish_type.id)
            return dish_type
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return None
    
    @session
    def delete_dish_type(self,session: Session, id: int) -> bool:
        dish_type = self.get_dish_type_by_id(session=session,id=id)
        
        if not dish_type:
            return False
        
        try:
            session.delete(dish_type)
            session.commit()
            
            return True
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return False