from fastapi import APIRouter,status,Path,Depends,HTTPException
from fastapi.responses import JSONResponse
from app.schemas.dish import DishTypeRequest,DishTypeResponse
from typing import List
from app.services import DishTypeService

router = APIRouter()

@router.get("/get_dishes_types",status_code=status.HTTP_200_OK)
def get_dishes_types(service: DishTypeService = Depends()) -> List[DishTypeResponse]:
    dishes_types_response = service.get_all()
    
    if not dishes_types_response:
        raise HTTPException(detail=f"Dishes Types not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[dish_type_response.model_dump() for dish_type_response in dishes_types_response],status_code=status.HTTP_200_OK)

@router.post("/create_dish_type",status_code=status.HTTP_201_CREATED)
def create_dish_type(dish_type_request: DishTypeRequest, service: DishTypeService = Depends()):
    dish_type = service.create_one(item_request=dish_type_request)
    
    if not dish_type:
        raise HTTPException(detail=f"Dish Type not Created",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(dish_type.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_dish_type/{id}",status_code=status.HTTP_200_OK)
def update_dish_type(dish_type_update: DishTypeRequest,id: int = Path(), service: DishTypeService = Depends()):

    dish_type = service.update_one_by_column_primary(value=id,item_update=dish_type_update)
    
    if not dish_type:
        raise HTTPException(detail=f"Dish Type not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(dish_type.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_dish_type/{id}",status_code=status.HTTP_200_OK)
def delete_dish_type(id: int = Path(), service: DishTypeService = Depends()):
    
    dish_type_deleted = service.delete_one(value=id)
    
    if not dish_type_deleted:
        raise HTTPException(detail=f"Dish Type not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content="Dish Type deleted",status_code=status.HTTP_200_OK)
