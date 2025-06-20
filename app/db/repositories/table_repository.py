from app.models import Table
from app.schemas.table import TableRequest,TableUpdate
from typing import List
from sqlalchemy.orm import Session
from app.db import session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class TableRepository:
    
    @session
    def get_tables(self,session: Session) -> List[Table]:
        try:
            query = select(Table)
            tables = session.execute(query).all()
            tables = [table[0] for table in tables]
            return tables
        except Exception as e:
            print(e)
        
        return None
    
    @session
    def get_table_by_id(self,session: Session,id:int) -> Table:
        try:
            query = select(Table).where(Table.id == id)
            table = session.execute(query).one()
            return table[0]
        except Exception as e:
            print(e)
        
        return None
    
    
    @session
    def create_table(self,session: Session, table_request: TableRequest) ->  Table | None:
        table_db = Table(
                name=table_request.name,
                state=table_request.state
            )
        try:
            session.add(table_db)
            session.commit()
            
            table = self.get_table_by_id(session=session,id=table_db.id)
            
            return table
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return None
    
    @session
    def update_table(self,session: Session, table_update: TableUpdate, id: int) -> Table | None:
        table = self.get_table_by_id(session=session,id=id)
        
        if not table:
            return None
        
        table_update = table_update.model_dump()
        try:
            for property,value in table_update.items():
                if value is not None:
                    setattr(table,property,value)
            session.commit()
            session.flush()
            table = self.get_table_by_id(session=session,id=table.id)
            return table
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return None
    
    @session
    def delete_table(self,session: Session, id: int) -> bool:
        table = self.get_table_by_id(session=session,id=id)
        
        if not table:
            return False
        
        try:
            session.delete(table)
            session.commit()
            
            return True
        except IntegrityError as e:
            session.rollback()
            print(e)
        
        return False