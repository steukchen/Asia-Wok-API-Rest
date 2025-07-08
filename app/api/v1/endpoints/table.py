from fastapi import APIRouter,status,Path,Depends,HTTPException
from fastapi.responses import JSONResponse
from app.schemas.table import TableResponse,TableRequest,TableUpdate
from typing import List
from app.services import TableService

router = APIRouter()

@router.get("/get_tables",status_code=status.HTTP_200_OK)
def get_tables(service: TableService = Depends()) -> List[TableResponse]:
    tables_response = service.get_all()
    
    if not tables_response:
        raise HTTPException(detail=f"Tables not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[table_response.model_dump() for table_response in tables_response],status_code=status.HTTP_200_OK)

@router.post("/create_table",status_code=status.HTTP_201_CREATED)
def create_table(table_request: TableRequest, service: TableService = Depends()):
    table = service.create_one(item_request=table_request)
    
    if not table:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Table not Created")
    
    return JSONResponse(table.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_table/{id}",status_code=status.HTTP_200_OK)
def update_table(table_update: TableUpdate,id: int = Path(), service: TableService = Depends()):
    table = service.update_one_by_column_primary(value=id,item_update=table_update)
    
    if not table:
        raise HTTPException(detail=f"Table not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(table.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_table/{id}",status_code=status.HTTP_200_OK)
def delete_table(id: int = Path(), service: TableService = Depends()):
    table_deleted = service.delete_one(value=id)
    
    if not table_deleted:
        raise HTTPException(detail=f"Table not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content="Table deleted",status_code=status.HTTP_200_OK)