from fastapi import APIRouter,status,HTTPException,Path,Depends
from fastapi.responses import JSONResponse
from typing import List
from app.schemas.customer import CustomerRequest,CustomerResponse,CustomerUpdate
from app.services import CustomerService

router = APIRouter()

@router.get("/get_customers",status_code=status.HTTP_200_OK)
def get_customers(service: CustomerService = Depends()) -> List[CustomerResponse]:
    customers = service.get_all()
    if not customers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customers not Found")
    
    return JSONResponse(content=[customer.model_dump() for customer in customers],status_code=status.HTTP_200_OK)

@router.get("/get_customer_by_id/{id}",status_code=status.HTTP_200_OK)
def get_customer_by_id(service: CustomerService = Depends(), id: int = Path(gt=0)) -> CustomerResponse:
    customer = service.get_one_by_column_primary(value=id)
    if not customer:
        raise HTTPException(detail="Customer Not Found.",status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=customer.model_dump(),status_code=status.HTTP_200_OK)

@router.post("/create_customer",status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerRequest,service: CustomerService = Depends()) -> CustomerResponse:
    customer = service.create_one(item_request=customer)
    if not customer:
        raise HTTPException(detail="Customer not Created.",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content=customer.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_customer/{id}",status_code=status.HTTP_200_OK)
def update_customer(customer: CustomerUpdate,id: int = Path(gt=0) ,service: CustomerService = Depends()) -> CustomerResponse:
    customer = service.update_one_by_column_primary(item_update=customer,value=id)
    if not customer:
        raise HTTPException(detail="Customer not Found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=customer.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_customer/{id}",status_code=status.HTTP_200_OK)
def delete_customer(id: int = Path(gt=0),service: CustomerService = Depends()) -> JSONResponse:
    is_deleted = service.delete_one(value=id)
    if not is_deleted:
        raise HTTPException(detail="Customer Not Deleted",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content="Customer Deleted",status_code=status.HTTP_200_OK)