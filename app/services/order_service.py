from .base_service import BaseService
from .dish_service import DishService
from .currency_service import CurrencyService
from app.schemas.order import OrderResponse,OrderRequest,OrderDishesResponse,OrderDishResponse,OrderDishesRequest,OrderCurrenciesRequest,OrderCurrenciesResponse,OrderCurrencyResponse
from app.db.repositories import OrderRepository
from typing import List, Union
from app.models import Order,Dish,DishType,Currency

class OrderService(BaseService):
    def __init__(self):
        self.response = OrderResponse
        self.repo = OrderRepository()
        
    def get_all(self,rol: str) -> List[OrderResponse] | None:
        if rol == "chef":
            state = ["pending","preparing"]
        else:
            state = ["pending","preparing","made"]
        items =self.repo.get_all_filter(state=state)
        if not items:
            return None
        return self._to_base_models(items_db=items) if items else None
    
    def get_orders_to_bill(self) -> List[OrderResponse] | None:
        items = self.repo.get_all_filter(state=["made","completed"])
        if not items:
            return None
        return self._to_base_models(items_db=items)
    
    def create_one(self,order_request: OrderRequest) -> OrderDishesResponse | None:
        # table_id = order_request.table_id
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
            notes=data[0].notes,
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
            notes=data[0].notes,
            table_id=data[0].table_id,
            state=data[0].state,
            dishes=[OrderDishResponse(
                dish=dish_service._to_base_model(item_db=[dish_detail[0],dish_detail[1]]),
                quantity=dish_detail[2]
            ) for dish_detail in data[1]]
        )
        
    def update_currencies(self,order_id: int,currencies: OrderCurrenciesRequest) -> OrderCurrenciesResponse:
        currencies = currencies.model_dump().pop("currencies")
        currencies = [[currency["currency_id"],currency["quantity"]] for currency in currencies]
        result = self.repo.update_currencies(currencies_data=currencies,order_id=order_id)
        
        return self._to_order_currencies_response(data=result)

    def get_one_with_currencies(self, order_id: int) -> OrderDishesResponse:
        result = self.repo.get_one_with_currencies(order_id=order_id)
        
        return self._to_order_currencies_response(data=result)
    
    def _to_order_currencies_response(self,data: List[ Union[Order,List[Union[Currency,int]]] ]):
        if not data[1]:
            return OrderCurrenciesResponse(
            id=data[0].id,
            customer_id=data[0].customer_id,
            order_date=data[0].order_date,
            created_by=data[0].created_by,
            notes=data[0].notes,
            table_id=data[0].table_id,
            state=data[0].state,
            currencies=[None]
        )
        
        currency_service = CurrencyService()
        return OrderCurrenciesResponse(
            id=data[0].id,
            customer_id=data[0].customer_id,
            order_date=data[0].order_date,
            created_by=data[0].created_by,
            notes=data[0].notes,
            table_id=data[0].table_id,
            state=data[0].state,
            currencies=[OrderCurrencyResponse(
                currency=currency_service._to_base_model(item_db=currency_detail[0]),
                quantity=currency_detail[1]
            ) for currency_detail in data[1]]
        )