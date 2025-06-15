from fastapi import APIRouter
from .endpoints import user

from app.models import insert_data_test

api_router = APIRouter()

@api_router.get("/data_test")
def data_test():
    insert_data_test()
    return True


api_router.include_router(user.router,prefix="/users",tags=["USERS"])