from fastapi import APIRouter,status,HTTPException,Depends,Path,Query
from fastapi.responses import JSONResponse
from app.schemas.order import OrderResponse,OrderRequest,OrderUpdate,OrderDishesRequest,OrderDishesResponse,OrderCurrenciesRequest,OrderCurrenciesResponse,OrdersFilter,OrderCurrencyResponse,OrdersDateFilter,CustomerDateFilter
from typing import List
from app.services import OrderService
from app.core.security import token_depend
from datetime import datetime

router = APIRouter()

@router.get("/get_orders",status_code=status.HTTP_200_OK)
def get_orders(data: token_depend,service: OrderService = Depends()) -> List[OrderResponse]:
    orders_response = service.get_all(rol=data["rol"])
    
    if not orders_response:
        raise HTTPException(detail="Orders not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[order.model_dump() for order in orders_response], status_code=status.HTTP_200_OK)

@router.get("/get_orders_by_date_customer_state",status_code=status.HTTP_200_OK)
def get_orders_by_date_customer_state(
        data: token_depend,
        filters: OrdersFilter = Query(),
        service: OrderService = Depends()
    ) -> List[OrderResponse]:
    if data["rol"]!="admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid rol"
        )
    print(filters)
    orders_response = service.get_by_date_customer_state(begin_date=filters.begin_date,end_date=filters.end_date,ci=filters.ci,state=filters.state)
    
    if not orders_response:
        raise HTTPException(detail="Orders not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[order.model_dump() for order in orders_response], status_code=status.HTTP_200_OK)


@router.get("/get_orders_to_bill",status_code=status.HTTP_200_OK)
def get_orders_to_bill(service: OrderService = Depends()) -> List[OrderResponse]:
    orders_response = service.get_orders_to_bill()
    
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
    # TableService().update_one_by_column_primary(TableUpdate(state="occupied"),order_request.table_id)
    
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
    
    print(dishes)
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

@router.get("/get_total_currencies_by_date",status_code=status.HTTP_200_OK)
def get_total_currencies_by_date(
        dates: OrdersDateFilter = Query(),
        service: OrderService = Depends()
    ) -> List[OrderCurrencyResponse]:
    
    currencies_response = service.get_total_currencies_by_date(begin_date=dates.begin_date,end_date=dates.end_date)
    
    if not currencies_response:
        raise HTTPException(detail="Currencies not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[currency.model_dump() for currency in currencies_response], status_code=status.HTTP_200_OK)

@router.get("/get_total_dishes_by_date",status_code=status.HTTP_200_OK)
def get_total_dishes_by_date(
        dates: OrdersDateFilter = Query(),
        service: OrderService = Depends()
    ) -> List[OrderCurrencyResponse]:
    
    dishes_response = service.get_total_dishes_by_date(begin_date=dates.begin_date,end_date=dates.end_date)
    
    if not dishes_response:
        raise HTTPException(detail="Dishes not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[dish.model_dump() for dish in dishes_response], status_code=status.HTTP_200_OK)

@router.get("/get_frequent_customers_by_date",status_code=status.HTTP_200_OK)
def get_frequent_customers_by_date(dates: CustomerDateFilter = Query(), service: OrderService = Depends()):
    customers_response = service.get_frequent_customers_by_date(number=dates.number,begin_date=dates.begin_date,end_date=dates.end_date)
    print(customers_response)
    if not customers_response:
        raise HTTPException(detail="Customers not Found.",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[customer.model_dump() for customer in customers_response], status_code=status.HTTP_200_OK)