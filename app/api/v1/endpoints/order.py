from fastapi import APIRouter,status,HTTPException,Depends,Path
from fastapi.responses import JSONResponse
from app.schemas.order import OrderResponse,OrderRequest,OrderUpdate,OrderDishesRequest,OrderDishesResponse,OrderCurrenciesRequest,OrderCurrenciesResponse
from typing import List
from app.services import OrderService,TableService
from app.core.security import token_depend
from app.schemas.table import TableUpdate

router = APIRouter()

@router.get("/get_orders",status_code=status.HTTP_200_OK)
def get_orders(data: token_depend,service: OrderService = Depends()) -> List[OrderResponse]:
    orders_response = service.get_all(rol=data["rol"])
    
    if not orders_response:
        raise HTTPException(detail="Orders not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[order.model_dump() for order in orders_response], status_code=status.HTTP_200_OK)

@router.get("/get_order_dishes/{id}",status_code=status.HTTP_200_OK)
def get_order_dishes(id: int = Path(gt=0),service: OrderService = Depends()) -> OrderDishesResponse:
    order_response = service.get_one_with_dishes(order_id=id)
    
    if not order_response:
        raise HTTPException(detail="Order not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=order_response.model_dump(), status_code=status.HTTP_200_OK)

@router.get("/get_order_currencies/{id}",status_code=status.HTTP_200_OK)
def get_order_currencies(id: int = Path(gt=0),service: OrderService = Depends()) -> OrderCurrenciesResponse:
    order_response = service.get_one_with_currencies(order_id=id)
    
    if not order_response:
        raise HTTPException(detail="Order not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=order_response.model_dump(), status_code=status.HTTP_200_OK)



@router.post("/create_order",status_code=status.HTTP_201_CREATED)
def create_order(data: token_depend,order_request: OrderRequest, service: OrderService = Depends()) -> OrderDishesResponse:
    order_request.created_by = data["id"]
    
    order = service.create_one(order_request=order_request)
    TableService().update_one_by_column_primary(TableUpdate(state="occupied"),order_request.table_id)
    
    if not order:
        raise HTTPException(detail=f"Order not created",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(order.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_order/{id}",status_code=status.HTTP_200_OK)
def update_order(order_update: OrderUpdate,id: int = Path(), service: OrderService = Depends()) -> OrderDishesResponse:

    order = service.update_one_by_column_primary(value=id,item_update=order_update)
    
    if not order:
        raise HTTPException(detail=f"Order not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(order.model_dump(),status_code=status.HTTP_200_OK)

@router.put("/update_dishes/{id}",status_code=status.HTTP_200_OK)
def update_dishes(dishes: OrderDishesRequest,id: int = Path(gt=0),service: OrderService = Depends()) -> OrderResponse:
    order = service.update_dishes(order_id=id,dishes=dishes)
    
    if not order:
        raise HTTPException(detail=f"Dishes not updated.",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(order.model_dump(),status_code=status.HTTP_200_OK)

@router.put("/update_currencies/{id}",status_code=status.HTTP_200_OK)
def update_currencies(currencies: OrderCurrenciesRequest, id: int = Path(gt=0), service: OrderService = Depends()) -> OrderCurrenciesResponse:
    order = service.update_currencies(order_id=id,currencies=currencies)

    if not order:
        raise HTTPException(detail=f"Currencies not updated.",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(order.model_dump(),status_code=status.HTTP_200_OK)
    
@router.delete("/delete_order/{id}",status_code=status.HTTP_200_OK)
def delete_order(id: int = Path(gt=0), service: OrderService = Depends()):
    
    order_deleted = service.delete_one(value=id)
    
    if not order_deleted:
        raise HTTPException(detail=f"Order not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content="Order deleted",status_code=status.HTTP_200_OK)
