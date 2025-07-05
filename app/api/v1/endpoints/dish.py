from fastapi import APIRouter,status,Path,Depends,HTTPException
from fastapi.responses import JSONResponse
from app.schemas.dish import DishResponse,DishRequest,DishUpdate
from typing import List
from app.services import DishService

router = APIRouter()

@router.get("/get_dishes",status_code=status.HTTP_200_OK)
def get_dishes(service: DishService = Depends()) -> List[DishResponse]:
    dishes_response = service.get_all()
    
    if not dishes_response:
        raise HTTPException(detail="Dishes not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[dish_response.model_dump() for dish_response in dishes_response])

@router.get("/get_dish_by_name/{name}",status_code=status.HTTP_200_OK)
def get_dish_by_name(name: str = Path(min_length=4),service: DishService = Depends()) -> List[DishResponse]:
    dishes_response = service.get_dishes_by_name(name=name)
    if not dishes_response:
        raise HTTPException(detail="Dish Not Found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[dish_response.model_dump() for dish_response in dishes_response])

@router.get("/get_dish_by_type/{type_id}",status_code=status.HTTP_200_OK)
def get_dish_by_name(type_id: int = Path(gt=0),service: DishService = Depends()) -> List[DishResponse]:
    dishes_response = service.get_dishes_by_type(type_id=type_id)
    if not dishes_response:
        raise HTTPException(detail="Dish Not Found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[dish_response.model_dump() for dish_response in dishes_response])

@router.post("/create_dish",status_code=status.HTTP_201_CREATED)
def create_dish(dish_request: DishRequest, service: DishService = Depends()):
    dish = service.create_one(item_request=dish_request)
    
    if not dish:
        raise HTTPException(detail=f"Dish not Created",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(dish.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_dish/{id}",status_code=status.HTTP_200_OK)
def update_dish(dish_update: DishUpdate,id: int = Path(), service: DishService = Depends()):

    dish = service.update_one_by_column_primary(value=id,item_update=dish_update)
    
    if not dish:
        raise HTTPException(detail=f"Dish not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(dish.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_dish/{id}",status_code=status.HTTP_200_OK)
def delete_dish(id: int = Path(), service: DishService = Depends()):
    
    dish_deleted = service.delete_one(value=id)
    
    if not dish_deleted:
        raise HTTPException(detail=f"Dish not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content="Dish deleted",status_code=status.HTTP_200_OK)
