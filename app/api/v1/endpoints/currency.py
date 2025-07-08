from fastapi import APIRouter,HTTPException,status,Path,Depends
from fastapi.responses import JSONResponse
from app.schemas.currency import CurrencyRequest,CurrencyResponse,CurrencyUpdate
from typing import List
from app.services import CurrencyService

router = APIRouter()

@router.get("/get_currencies",status_code=status.HTTP_200_OK)
def get_currencies(service: CurrencyService = Depends()) -> List[CurrencyResponse]:
    currencies = service.get_all()
    if not currencies:
        raise HTTPException(detail="Currencies not Found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[currency.model_dump() for currency in currencies],status_code=status.HTTP_200_OK)

@router.post("/create_currency",status_code=status.HTTP_201_CREATED)
def create_currency(currency: CurrencyRequest,service: CurrencyService = Depends()) -> CurrencyResponse:
    currency = service.create_one(item_request=currency)
    if not currency:
        raise HTTPException(detail="Currency not Created",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content=currency.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_currency/{id}",status_code=status.HTTP_200_OK)
def update_currency(currency: CurrencyUpdate,id: int = Path(gt=0),service: CurrencyService = Depends()) -> CurrencyResponse:
    currency = service.update_one_by_column_primary(item_update=currency,value=id)
    if not currency:
        raise HTTPException(detail="Currency not Found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=currency.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_currency/{id}",status_code=status.HTTP_200_OK)
def delete_currency(id: int = Path(gt=0), service: CurrencyService = Depends()) -> CurrencyResponse:
    is_deleted = service.delete_one(value=id)
    if not is_deleted:
        raise HTTPException(detail="Currency not Deleted",status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content="Currency Deleted.",status_code=status.HTTP_200_OK)
        