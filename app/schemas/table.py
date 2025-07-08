from pydantic import BaseModel,field_validator

class TableResponse(BaseModel):
    id: int
    name: str
    state: str
    
    
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": 1,
                    "name": "MESA 1",
                    "state": "enabled"
                }
            }
    }
    

class TableRequest(BaseModel):
    name: str
    state: str
    
    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        value =value.upper()
        
        if len(value) <= 4:
            raise ValueError("The name must be longer than 4 characters.")
        
        return value
    
    @field_validator("state")
    def validate_state(cls,value:str):
        states = 'enabled','disabled','occupied','reserved'
        
        value = value.lower()
        if value not in states:
            raise ValueError("Invalid State.")
        
        return value
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "name": "MESA 1",
                    "state": "enabled"
                }
            }
    }
    
class TableUpdate(TableRequest):
    name: str = None
    state: str = None