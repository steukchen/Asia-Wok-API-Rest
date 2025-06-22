from app.db.repositories import TableRepository
from typing import List
from app.schemas.table import TableResponse,TableRequest,TableUpdate

class TableService:
    def __init__(self):
        self.repo = TableRepository()
    
    def get_tables(self,) -> List[TableResponse]:
        tables_db = self.repo.get_tables()
        if not tables_db:
            return None
        tables_response = [TableResponse(
            id=table_db.id,
            name=table_db.name,
            state=table_db.state,
        ) for table_db in tables_db]
        return tables_response
    
    def create_table(self,table_request: TableRequest) -> TableResponse | None:
        table = self.repo.create_table(table_request=table_request)
        
        if not table:
            return None
        
        return TableResponse(
            id=table.id,
            name=table.name,
            state=table.state,
        )
    
    def update_table(self,table_update: TableUpdate, id: int):
        table = self.repo.update_table(table_update=table_update,id=id)
        
        if not table:
            return None
        
        return TableResponse(
            id=table.id,
            name=table.name,
            state=table.state,
        )
        
    def delete_table(self,id: int) -> bool:
        
        table_deleted = self.repo.delete_table(id=id)
        
        if not table_deleted:
            return False
        
        return True
