from pydantic import BaseModel, field_validator,field_serializer,model_validator
from datetime import date,datetime,timedelta,timezone
from .dish import DishResponse
from .currency import CurrencyResponse
from .table import TableResponse
from typing import List
from re import match

class OrderResponse(BaseModel):
    id: int
    customer_id: int | None
    order_date: datetime
    created_by: str
    notes: str | None = None
    table: TableResponse
    state: str
    
    @field_validator("created_by",mode="before")
    def validate_id(cls,value):
        return str(value)
    
    # Tranformar a hora caracas
    @field_validator("order_date")
    def validate_order_date(cls,value: datetime):
        return value.astimezone(timezone(timedelta(hours=-4)))
    
    @field_serializer("order_date")
    def serialize_order_date(self,value: datetime):
        return value.strftime("%m/%d/%Y, %H:%M:%S")
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": 1,
                    "customer_id": 1,
                    "order_date": "MM/DD/YYYY hh:mm:ss",
                    "created_by": "76ff5576-f9c2-4b85-844e-dff1b3b9a3dd",
                    "table_id": 1,
                    "state": "pending",
                }
            }
    }

class OrderDishResponse(BaseModel):
    dish: DishResponse
    quantity: int

class OrderDishesResponse(OrderResponse):
    dishes: List[OrderDishResponse] | List

    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": 1,
                    "customer_id": 1,
                    "order_date": "MM/DD/YYYY hh:mm:ss",
                    "created_by": "76ff5576-f9c2-4b85-844e-dff1b3b9a3dd",
                    "table_id": 1,
                    "state": "pending",
                    "dishes": [
                        {
                            "dish": {
                                "id": 1,
                                "name": "Chop Suey",
                                "description":"Comida muy rica asiatica",
                                "price": 2.45,
                                "type": 1
                            },
                            "quantity": 2
                        },
                    ]
                    
                }
            }
    }

class OrderBase(BaseModel):
    customer_id: int = None
    # order_date: datetime = datetime.now()
    created_by: str | None = None
    table_id: int
    notes: str | None = None
    state: str = "pending"
    
    @field_validator("customer_id","table_id")
    def validate_id(cls,value: int) -> int:
        if value <= 0:
            raise ValueError("Customer_id and Table_id must be greather than 0.")

        return value
    
    @field_validator("created_by")
    def validate_created_by(cls,value: str) -> str:
        if len(value) < 10:
            raise ValueError("Created_by must be 10 characteres or more")
        
        return value
    
    @field_validator("state")
    def validate_state(cls,value: str) -> str:
        value = value.lower()
        states = 'pending','preparing','made','completed','cancelled'
        if value not in states:
            raise ValueError("Invalid State.")
        
        return value
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "customer_id": 1,
                    "order_date": datetime.now(),
                    "table_id": 1,
                    "notes": "",
                    "state": "pending",
                }
            }
    }

class OrderDishRequest(BaseModel):
    dish_id: int
    quantity: int 
    
    @field_validator("dish_id")
    def validate_dish_id(cls,value: int) -> int:
        if value <= 0:
            raise ValueError("Invalid dish_id")
        
        return value

    @field_validator("quantity")
    def validate_quantity(cls,value: int) -> int:
        if value < 0:
            raise ValueError("Invalid quantity")
        
        return value

class OrderDishesRequest(BaseModel):
    dishes: List[OrderDishRequest]
    
    @field_validator("dishes")
    def validate_dishes(cls,value: List[OrderDishRequest]) -> List[OrderDishRequest]:
        for i in value:
            if len(tuple(filter(lambda x: x.dish_id == i.dish_id,value))) > 1:
                raise ValueError("Dish_id repeated")
        
        return value
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "dishes": [
                        {
                            "dish_id":1,
                            "quantity":2
                        },
                        {
                            "dish_id":2,
                            "quantity":1
                        }
                    ]
                }
            }
    }

class OrderRequest(OrderBase,OrderDishesRequest):
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "customer_id": 1,
                    "order_date": datetime.now(),
                    "table_id": 1,
                    "state": "pending",
                    "notes": "Notes",
                    "dishes": [
                        {
                            "dish_id":1,
                            "quantity":2
                        },
                        {
                            "dish_id":2,
                            "quantity":1
                        }
                    ]
                }
            }
    }
    
class OrderUpdate(OrderBase):
    customer_id: int = None
    # order_date: datetime = None
    notes: str = None
    created_by: str = None
    table_id: int = None
    state: str = None
    

class OrderCurrencyRequest(BaseModel):
    currency_id: int
    quantity: float 
    
    @field_validator("currency_id")
    def validate_currency_id(cls,value: int) -> int:
        if value <= 0:
            raise ValueError("Invalid currency_id")
        
        return value

    @field_validator("quantity")
    def validate_quantity(cls,value: float) -> float:
        if value < 0:
            raise ValueError("Invalid quantity")
        
        return value    

class OrderCurrenciesRequest(BaseModel):
    currencies: List[OrderCurrencyRequest]
    
class OrderCurrencyResponse(BaseModel):
    currency: CurrencyResponse
    quantity: float
    
class OrderCurrenciesResponse(OrderResponse):
    currencies: List[OrderCurrencyResponse] | List

    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": 1,
                    "customer_id": 1,
                    "order_date": "MM/DD/YYYY hh:mm:ss",
                    "created_by": "76ff5576-f9c2-4b85-844e-dff1b3b9a3dd",
                    "table_id": 1,
                    "state": "pending",
                    "currencies": [
                        {
                            "currency": {
                                "id": 1,
                                "name": "DOLAR",
                                "exchange": 1
                            },
                            "quantity": 3.2
                        },
                    ]
                    
                }
            }
    }
    

class OrdersDateFilter(BaseModel):
    begin_date: date
    end_date: date 
    
class OrdersFilter(BaseModel):
    begin_date: date = None
    end_date: date = None
    ci: str = None
    state: str = None
    
    @field_validator("ci")
    def validate_ci(cls,value:str):
        value = value.upper()
        regex = r"^[A-Z]-\d{7,8}$"
        if not bool(match(regex,value)):
            raise ValueError("The CI does not comply with the appropriate format")
        return value
    
    @field_validator("state")
    def validate_state(cls,value: str) -> str:
        value = value.lower()
        states = 'pending','preparing','made','completed','cancelled'
        if value not in states:
            raise ValueError("Invalid State.")
        
        return value
    
    @field_validator('end_date')
    def validate_end_date(cls, v:date,info) -> date:
        if v is None:
            return None
        begin_date = info.data['begin_date']
        
        if begin_date is None:
            return None
    
        
        if v < begin_date:
            raise ValueError('begin_date must be less than end_date')
        return v
    
    @model_validator(mode='after')
    def check_at_least_one_filter(cls, values):
        # Verificamos que al menos uno de los campos no sea None
        data = values.model_dump().values()
        if all(value is None for value in data):
            raise ValueError('At least one filter must be provided')
        return values
    

class CustomerDateFilter(OrdersDateFilter):
    number: int = 10