from fastapi import APIRouter
from .endpoints import dish_type, user, table, customer

from app.models import insert_data_test

api_router = APIRouter()

@api_router.get("/data_test")
def data_test():
    insert_data_test()
    return True


api_router.include_router(user.router,prefix="/users",tags=["USERS"])
api_router.include_router(table.router,prefix="/tables",tags=["TABLES"])
api_router.include_router(dish_type.router,prefix="/dishes_types",tags=["DISHES_TYPES"])
api_router.include_router(customer.router,prefix="/customers",tags=["CUSTOMERS"])