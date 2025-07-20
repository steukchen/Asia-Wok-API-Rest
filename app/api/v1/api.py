from fastapi import APIRouter,Depends
from .endpoints import dish_type, user, table, customer, currency,dish,order,security
from app.core.security import get_data_token
from .websocket import ws


api_router = APIRouter()
api_router_private = APIRouter(dependencies=[Depends(get_data_token)])


api_router_private.include_router(user.router,prefix="/users",tags=["USERS"])
api_router_private.include_router(table.router,prefix="/tables",tags=["TABLES"])
api_router_private.include_router(dish_type.router,prefix="/dishes_types",tags=["DISHES_TYPES"])
api_router_private.include_router(customer.router,prefix="/customers",tags=["CUSTOMERS"])
api_router_private.include_router(currency.router,prefix="/currencies",tags=["CURRENCIES"])
api_router_private.include_router(dish.router,prefix="/dishes",tags=["DISHES"])
api_router_private.include_router(order.router,prefix="/orders",tags=["ORDERS"])
api_router.include_router(security.router,prefix="",tags=["SECURITY"])
api_router.include_router(ws.router,prefix="",tags=["WEBSOCKET"])
api_router.include_router(api_router_private)