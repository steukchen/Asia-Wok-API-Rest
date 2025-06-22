from app.models import Table
from app.schemas.table import TableRequest,TableUpdate
from typing import List
from sqlalchemy.orm import Session
from app.db import session
from sqlalchemy import select

class TableRepository:
    
    @session
    def get_tables(self,session: Session) -> List[Table]:
        query = select(Table)
        tables = session.execute(query).all()
        if not tables:
            return None
        tables = [table[0] for table in tables]
        return tables
    
    @session
    def get_table_by_id(self,session: Session,id:int) -> Table | None:
        query = select(Table).where(Table.id == id)
        table = session.execute(query).fetchone()
        if not table:
            return None
        
        return table[0]
    
    
    @session
    def create_table(self,session: Session, table_request: TableRequest) ->  Table:
        table_db = Table(
                name=table_request.name,
                state=table_request.state
            )
        session.add(table_db)
        
        return table_db
    
    @session
    def update_table(self,session: Session, table_update: TableUpdate, id: int) -> Table | None:
        table = self.get_table_by_id(session=session,id=id)
        
        if not table:
            return None
        
        table_update = table_update.model_dump()
        for property,value in table_update.items():
            if value is not None:
                setattr(table,property,value)
        return table
    
    @session
    def delete_table(self,session: Session, id: int) -> bool:
        table = self.get_table_by_id(session=session,id=id)
        
        if table:
            session.delete(table)
        return table is not None