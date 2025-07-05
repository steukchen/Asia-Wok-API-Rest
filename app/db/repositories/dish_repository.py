from app.models import Dish,DishType
from app.schemas.dish import DishRequest,DishUpdate
from .base_repository import BaseRepository
from .dish_type_repository import DishTypeRepository
from app.db import session
from typing import List,Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select,join
from sqlalchemy.sql.operators import ilike_op
from sqlalchemy.engine import Row

class DishRepository(BaseRepository):
    def __init__(self):
        self.base = Dish
    
    @session
    def get_dishes(self,session: Session) -> List[Tuple[Dish,DishType]]:
        query = select(Dish,DishType).join(DishType,Dish.type_id==DishType.id)
        data = session.execute(query).fetchall()
        if not data:
            return None
        return data
    
    @session
    def get_dishes_by_type(self,session: Session,type_id: int) -> List[Tuple[Dish,DishType]]:
        query = (
            select(Dish,DishType).join(DishType,Dish.type_id==DishType.id)
            .where(Dish.type_id==type_id)
        )
        data = session.execute(query).fetchall()
        
        if not data:
            return None
        
        return data
    
    @session
    def get_dishes_by_name(self,session: Session, name: str) -> List[Tuple[Dish,DishType]]:
        query = (
            select(Dish,DishType).join(DishType,Dish.type_id==DishType.id)
            .where(ilike_op(Dish.name,f"%{name}%"))
        )
        
        data = session.execute(query).fetchall()
        
        if not data:
            return None
        
        return data
    
    @session
    def create_one(self,session: Session, data: DishRequest) -> Tuple[Dish,DishType]:
        dish: Dish = super().create_one(session=session,data=data)
        if not dish:
            return None
        
        dish_type_repo = DishTypeRepository()
        dish_type = dish_type_repo.get_one_by_column_primary(session=session,value=dish.type_id)
        
        return (dish,dish_type)
    
    @session
    def update_one_by_column_primary(self,session: Session, data: DishUpdate,value: int):
        dish: Dish = super().update_one_by_column_primary(data=data,value=value)
        if not dish:
            return None
        
        dish_type_repo = DishTypeRepository()
        dish_type = dish_type_repo.get_one_by_column_primary(session=session,value=dish.type_id)
        
        return (dish,dish_type)