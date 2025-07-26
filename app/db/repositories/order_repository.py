from app.models import Order,OrderDish,DishType,Dish,Currency,OrderCurrency
from .base_repository import BaseRepository
from app.db import session,ExceptionRepository
from sqlalchemy.orm import Session
from typing import List,Union
from sqlalchemy import select,desc
from sqlalchemy.sql.functions import sum

class OrderRepository(BaseRepository):
    def __init__(self):
        self.base = Order
    
    @session
    def get_all_filter(self,session: Session,state:List[str]) -> List[Order] | None:
        query = select(Order).where(Order.state.in_(state))
        items = session.execute(query).all()
        if not items:
            return None
        
        return [item[0] for item in items]
    
    
    @session
    def create_with_dishes(self,session: Session, order_request: dict,dishes_data: List[List[int]]) -> List[ Union[Order,List[List[Union[Dish,int]]]] ]:
        order_db: Order = self.create_one(session=session,data=order_request)
        if not order_db:
            return ExceptionRepository(message="Order Not Created",code=400)
        
        dishes = self.add_dishes(session=session,dishes_data=dishes_data,order_id=order_db.id)
        if not dishes:
            return ExceptionRepository(message="Invalid Dishes",code=409)

        session.flush()
        return self.get_one_with_dishes(session=session,order_id=order_db.id) 
    
    @session 
    def add_dishes(self,session: Session,order_id: int,dishes_data: List[List[int]]) -> bool:
        if bool(tuple(filter(lambda x: x[1] <= 0,dishes_data))):
            raise ExceptionRepository(message="Invalid quantity",code=409)

        dishes_ids = [i[0] for i in dishes_data]
        dishes_ids.sort()
        
        query = (
            select(Dish)
            .where(Dish.id.in_(dishes_ids))
            .order_by(desc(Dish.id))
        )
        dishes_db = session.execute(query).fetchall()
        
        if len(dishes_db) != len(dishes_data):
            session.rollback()
            raise ExceptionRepository(message="Invalid Dishes",code=409)
        
        dishes_result = [[d,dt[1]] for d,dt in zip(dishes_db,dishes_data)]
        
        order_dishes_db = [OrderDish(
            order_id = order_id,
            dish_id= dish[0][0].id,
            price= dish[0][0].price,
            quantity = dish[1]
            
        ) for dish in dishes_result]
        
        session.add_all(order_dishes_db)
        
        
        return True
    
    @session
    def update_dishes(self,session: Session, order_id: int, dishes_data: List[List[int]]) -> bool:
        order_db: Order = self.get_one_by_column_primary(session=session,value=order_id)
        if not order_db:
            raise ExceptionRepository(message="Order Not Found",code=404)
        
        dishes_ids = [i[0] for i in dishes_data]
        dishes_ids.sort()
        query = (
            select(OrderDish)
            .where(OrderDish.dish_id.in_(dishes_ids),OrderDish.order_id==order_db.id)
            .order_by(desc(OrderDish.id))
        )
        
        repeated_dishes = session.execute(query).fetchall()
        
        if repeated_dishes:
            for dish in repeated_dishes:
                dish_data = list(filter(lambda x: x[0]==dish[0].dish_id, dishes_data))[0]
                quantity = dish_data[1]
                dish[0].quantity = quantity
                if dish[0].quantity <= 0:
                    session.delete(dish[0])
                dishes_data.remove(dish_data)
                dishes_ids.remove(dish_data[0])
                session.flush([dish[0]])
        
        if len(dishes_data) > 0:
            self.add_dishes(session=session,order_id=order_id,dishes_data=dishes_data)
            session.flush()
        
        return self.get_one_with_dishes(session=session,order_id=order_db.id)
    
    @session
    def get_one_with_dishes(self,session: Session,order_id: int) -> List[ Union[Order,List[Union[Dish,DishType,int]]] ]:
        order_db: Order = self.get_one_by_column_primary(session=session,value=order_id)
        if not order_db:
            raise ExceptionRepository(message="Order Not Found",code=404)
        query = (
                select(Dish,DishType,sum(OrderDish.quantity))
                .join(Dish,Dish.id==OrderDish.dish_id)
                .join(DishType,Dish.type_id==DishType.id)
                .where(OrderDish.order_id==order_id)
                .group_by(Dish.id,DishType.id)
        )
        
        result = list(session.execute(query).fetchall())
        
        if not result:
            result = None
        
        return [order_db,result]
    
    @session
    def delete_one_by_column_primary(self,session: Session, value: int) -> bool:
        query = select(OrderDish).where(OrderDish.order_id==value)
        dishes = session.execute(query).fetchall()
        for dish in dishes: 
            session.delete(dish[0])
        session.flush()
        query = select(OrderCurrency).where(OrderCurrency.order_id==value)
        currencies = session.execute(query).fetchall()
        for currency in currencies: 
            session.delete(currency[0])
        session.flush()
        is_deleted = super().delete_one_by_column_primary(session=session,value=value)
        return is_deleted is not None
    
    @session
    def get_one_with_currencies(self,session: Session,order_id: int) -> List[ Union[Order,List[Union[Currency,int]]] ]:
        order_db: Order = self.get_one_by_column_primary(session=session,value=order_id)
        if not order_db:
            raise ExceptionRepository(message="Order Not Found",code=404)
        query = (
                select(Currency,sum(OrderCurrency.quantity))
                .join(Currency,Currency.id==OrderCurrency.currency_id)
                .where(OrderCurrency.order_id==order_id)
                .group_by(Currency.id)
        )
        
        result = list(session.execute(query).fetchall())
        
        if not result:
            result = None
        
        return [order_db,result]
    
    @session 
    def add_currencies(self,session: Session,order_id: int,currencies_data: List[List[int]]) -> bool:
        if bool(tuple(filter(lambda x: x[1] <= 0,currencies_data))):
            raise ExceptionRepository(message="Invalid quantity",code=409)

        currencies_ids = [i[0] for i in currencies_data]
        currencies_ids.sort()
        
        query = (
            select(Currency)
            .where(Currency.id.in_(currencies_ids))
            .order_by(desc(Currency.id))
        )
        currencies_db = session.execute(query).fetchall()
        
        if len(currencies_db) != len(currencies_data):
            session.rollback()
            raise ExceptionRepository(message="Invalid Currencies",code=409)
        
        currencies_result = [[c,ct[1]] for c,ct in zip(currencies_db,currencies_data)]
        
        order_currencies_db = [OrderCurrency(
            order_id = order_id,
            currency_id= currency[0][0].id,
            exchange= currency[0][0].exchange,
            quantity = currency[1]
            
        ) for currency in currencies_result]
        
        session.add_all(order_currencies_db)
        
        
        return True
    
    @session
    def update_currencies(self,session: Session, order_id: int, currencies_data: List[List[int]]) -> bool:
        order_db: Order = self.get_one_by_column_primary(session=session,value=order_id)
        if not order_db:
            raise ExceptionRepository(message="Order Not Found",code=404)
        
        currencies_ids = [i[0] for i in currencies_data]
        currencies_ids.sort()
        query = (
            select(OrderCurrency)
            .where(OrderCurrency.currency_id.in_(currencies_ids),OrderCurrency.order_id==order_db.id)
            .order_by(desc(OrderCurrency.id))
        )
        
        repeated_currencies = session.execute(query).fetchall()
        
        if repeated_currencies:
            for currency in repeated_currencies:
                currency_data = list(filter(lambda x: x[0]==currency[0].currency_id, currencies_data))[0]
                quantity = currency_data[1]
                currency[0].quantity = quantity
                if currency[0].quantity <= 0:
                    session.delete(currency[0])
                currencies_data.remove(currency_data)
                currencies_ids.remove(currency_data[0])
                session.flush([currency[0]])
        
        if len(currencies_data) > 0:
            self.add_currencies(session=session,order_id=order_id,currencies_data=currencies_data)
            session.flush()
        
        return self.get_one_with_currencies(session=session,order_id=order_db.id)