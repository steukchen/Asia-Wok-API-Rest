from app.models import Base
from typing import List
from app.db.session import session
from sqlalchemy.orm import Session
from sqlalchemy import select

class BaseRepository:
    base: Base
    column_primary: str = "id"
    
    @session
    def get_all(self,session: Session) -> List[Base] | None:
        query = select(self.base)
        items = session.execute(query).all()
        if not items:
            return None
        
        return [item[0] for item in items]
    
    @session
    def get_one_by_column_primary(self,session: Session, value: any) -> Base | None:
        query = select(self.base).where(getattr(self.base,self.column_primary) == value)
        item = session.execute(query).fetchone()
        if not item:
            return None
        return item[0]
    
    @session
    def get_one_by_column(self,session: Session,column: str, value: any) -> Base | None:
        query = select(self.base).where(getattr(self.base,column) == value)
        item = session.execute(query).fetchone()
        if not item:
            return None
        return item[0]
    
    @session
    def create_one(self,session: Session, data: dict) -> Base:
        item = self.base(
            **data
        )
        session.add(item)
        session.flush([item])
        
        return item

    @session
    def update_one_by_column_primary(self,session: Session, value: any, data: dict) -> Base | None:
        item = self.get_one_by_column_primary(session=session,value=value)
        
        if not item:
            return None
        
        for property,v in data.items():
            if v is not None:
                setattr(item,property,v)
                
        return item
    
    @session
    def delete_one_by_column_primary(self,session: Session, value: any) -> bool:
        item = self.get_one_by_column_primary(session=session,value=value)
        
        if item:
            session.delete(item)
        
        return item is not None