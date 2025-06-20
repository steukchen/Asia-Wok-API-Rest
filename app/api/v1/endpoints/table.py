from fastapi import APIRouter,status,Path
from fastapi.responses import JSONResponse
from app.schemas.table import TableResponse,TableRequest,TableUpdate
from typing import List
from app.services import TableService

router = APIRouter()

@router.get("/get_tables",status_code=status.HTTP_200_OK)
def get_tables() -> List[TableResponse]:
    service = TableService()
    tables_response = service.get_tables()
    
    if not tables_response:
        return JSONResponse(content=f"There aren't tables registered",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[table_response.model_dump() for table_response in tables_response],status_code=status.HTTP_200_OK)

@router.post("/create_table",status_code=status.HTTP_201_CREATED)
def create_table(table_request: TableRequest):
    service = TableService()
    table = service.create_table(table_request=table_request)
    
    if not table:
        return JSONResponse("Table not Created",status_code=status.HTTP_409_CONFLICT)
    
    return JSONResponse(table.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_table/{id}",status_code=status.HTTP_200_OK)
def update_table(table_update: TableUpdate,id: int = Path()):
    service = TableService()

    table = service.update_table(id=id,table_update=table_update)
    
    if not table:
        return JSONResponse("Table not Updated",status_code=status.HTTP_409_CONFLICT)
    
    return JSONResponse(table.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_table/{id}",status_code=status.HTTP_200_OK)
def delete_table(id: int = Path()):
    service = TableService()
    
    table_deleted = service.delete_table(id=id)
    
    if not table_deleted:
        return JSONResponse("Table not deleted",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content="Table deleted",status_code=status.HTTP_200_OK)