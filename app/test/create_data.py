from app.models import create_structure
from app.services import UserService,DishService,DishTypeService,CustomerService,CurrencyService,TableService,OrderService
from app.schemas.user import UserRequest
from app.schemas.dish import DishRequest,DishTypeRequest
from app.schemas.currency import CurrencyRequest
from app.schemas.customer import CustomerRequest
from app.schemas.order import OrderRequest,OrderDishRequest
from app.schemas.table import TableRequest

import asyncio


async def create_data():
    
    await create_structure()
    user_service = UserService()
    user = user_service.create_one(item_request=UserRequest(
        username="HARSUE",
        email="harsue0311@gmail.com",
        rol="admin",
        status=True,
        password="Pass123.."
    ))
    
    dish_type_service = DishTypeService()
    type_1 = dish_type_service.create_one(item_request=DishTypeRequest(name="ENTRADA"))
    type_2 = dish_type_service.create_one(item_request=DishTypeRequest(name="PLATO FUERTE"))
    
    dish_service = DishService()
    dish_1 = dish_service.create_one(item_request=DishRequest(
        name="Rollitos Primavera",
        description="Unos rollitos burda de lo malandro",
        price=2.20,
        type_id=type_2.id
    ))
    dish_2 = dish_service.create_one(item_request=DishRequest(
        name="Dorilocos",
        description="Doritos pero locos",
        price=2.20,
        type_id=type_1.id
    ))
    
    customer = CustomerService().create_one(CustomerRequest(
        ci="V-32325849",
        name="Harwing",
        lastname="Martinez",
        phone_number="04161797833",
        address="El palmar de la cope"
    ))
    
    currency_service = CurrencyService()
    dolar = currency_service.create_one(CurrencyRequest(
        name="DOLAR",
        exchange="1"
    ))
    bs = currency_service.create_one(CurrencyRequest(
        name="Bolivar",
        exchange="102"
    ))
    cop = currency_service.create_one(CurrencyRequest(
        name="COP",
        exchange="4000"
    ))
    
    table_service = TableService()
    table_1 = table_service.create_one(TableRequest(
        name="MESA 1",
        state="enabled"
    ))
    table_2 = table_service.create_one(TableRequest(
        name="MESA 2",
        state="enabled"
    ))
    table_3 = table_service.create_one(TableRequest(
        name="MESA 3",
        state="enabled"
    ))
    
    OrderService().create_one(OrderRequest(
        dishes=[
            OrderDishRequest(dish_id=dish_1.id,quantity=2),
            OrderDishRequest(dish_id=dish_2.id,quantity=4)
        ],
        customer_id=customer.id,
        created_by=user.id,
        table_id=table_1.id,
        
    ))
    

if __name__=="__main__":
    asyncio.run(create_data()) 