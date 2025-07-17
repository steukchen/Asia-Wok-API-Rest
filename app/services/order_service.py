from .base_service import BaseService
from .dish_service import DishService
from app.schemas.order import OrderResponse,OrderRequest,OrderDishesResponse,OrderDishResponse,OrderDishesRequest
from app.db.repositories import OrderRepository
from typing import List, Union
from app.models import Order,Dish,DishType

class OrderService(BaseService):
    def __init__(self):
        self.response = OrderResponse
        self.repo = OrderRepository()
    
    def create_one(self,order_request: OrderRequest) -> OrderDishesResponse | None:
        order_request = order_request.model_dump()
        dishes = order_request.pop("dishes")
        dishes = [[dish["dish_id"],dish["quantity"]] for dish in dishes]
        
        result = self.repo.create_with_dishes(dishes_data=dishes,order_request=order_request)
        return self._to_order_dishes_response(data=result)
    
    def update_dishes(self,order_id: int,dishes: OrderDishesRequest) -> OrderDishesResponse:
        dishes = dishes.model_dump().pop("dishes")
        dishes = [[dish["dish_id"],dish["quantity"]] for dish in dishes]
        result = self.repo.update_dishes(dishes_data=dishes,order_id=order_id)
        
        return self._to_order_dishes_response(data=result)

    def get_one_with_dishes(self, order_id: int) -> OrderDishesResponse:
        result = self.repo.get_one_with_dishes(order_id=order_id)
        
        return self._to_order_dishes_response(data=result)
    
    def _to_order_dishes_response(self,data: List[ Union[Order,List[Union[Dish,DishType,int]]] ]):
        if not data[1]:
            return OrderDishesResponse(
            id=data[0].id,
            customer_id=data[0].customer_id,
            order_date=data[0].order_date,
            created_by=data[0].created_by,
            table_id=data[0].table_id,
            state=data[0].state,
            dishes=[None]
        )
        
        dish_service = DishService()
        return OrderDishesResponse(
            id=data[0].id,
            customer_id=data[0].customer_id,
            order_date=data[0].order_date,
            created_by=data[0].created_by,
            table_id=data[0].table_id,
            state=data[0].state,
            dishes=[OrderDishResponse(
                dish=dish_service._to_base_model(item_db=[dish_detail[0],dish_detail[1]]),
                quantity=dish_detail[2]
            ) for dish_detail in data[1]]
        )