from ..db.repositories import BaseRepository
from pydantic import BaseModel
from typing import List

class BaseService:
    response: BaseModel
    
    def __init__(self):
        self.repo = BaseRepository()
        
    def get_all(self) -> List[BaseModel] | None:
        items_db = self.repo.get_all()
        if not items_db:
            return None
        items_db = [self.response(
            **{
                f"{key}":getattr(item_db,key) 
                for key in self.response.model_construct().model_json_schema()["properties"].keys()
            }  
        ) for item_db in items_db ]
        return items_db
    
    def get_one_by_column_primary(self, value: any) -> BaseModel | None:
        item_db = self.repo.get_one_by_column_primary(value=value)
        if not item_db:
            return None
        
        return self.response(
            **{
                f"{key}":getattr(item_db,key) 
                for key in self.response.model_construct().model_json_schema()["properties"].keys()
            }
        )
    
    def get_one_by_column(self, column: str, value: any) -> BaseModel | None:
        item_db = self.repo.get_one_by_column(column=column,value=value)
        if not item_db:
            return None
        
        return self.response(
            **{
                f"{key}":getattr(item_db,key) 
                for key in self.response.model_construct().model_json_schema()["properties"].keys()
            }
        )
    
    def create_one(self,item_request: BaseModel) -> BaseModel | None:
        item_db = self.repo.create_one(data=item_request)
        
        if not item_db:
            return None
        
        return self.response(
            **{
                f"{key}":getattr(item_db,key) 
                for key in self.response.model_construct().model_json_schema()["properties"].keys()
            }
        )
    
    def update_one_by_column_primary(self,item_update: BaseModel, value: any) -> BaseModel | None:
        item_db = self.repo.update_one_by_column_primary(data=item_update,value=value)
        
        if not item_db:
            return None
        
        return self.response(
            **{
                f"{key}":getattr(item_db,key) 
                for key in self.response.model_construct().model_json_schema()["properties"].keys()
            }
        )
        
    def delete_one(self,value: any) -> bool:
        
        item_deleted = self.repo.delete_one_by_column_primary(value=value)
        
        if not item_deleted:
            return False
        
        return True