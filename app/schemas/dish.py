from pydantic import BaseModel,field_validator#,field_serializer
# from datetime import datetime

class DishTypeResponse(BaseModel):
    id: int
    name: str
    # created_at: datetime
    # updated_at: datetime
    
    # @field_serializer("created_at","updated_at")
    # def serialize_created_at(self,value: datetime):
    #     print(value)
    #     return value.strftime("%d/%m/%Y, %H:%M:%S")
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": 1,
                    "name": "BEBIDA"
                }
            }
    }
    

class DishTypeRequest(BaseModel):
    name: str
    
    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        value =value.upper()
        
        if len(value) <= 4:
            raise ValueError("The name must be longer than 4 characters.")
        
        return value
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "name": "BEBIDA",
                }
            }
    }

class DishResponse(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    type: DishTypeResponse
    status: bool
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": 1,
                    "name": "Chop Suey",
                    "description":"Comida muy rica asiatica",
                    "price": 2.45,
                    "type": 1,
                    "status": True
                }
            }
    }

class DishRequest(BaseModel):
    name: str
    description: str = None
    price: float
    type_id: int
    status: bool = True
    
    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        value = value.upper()
        
        if len(value) <= 4:
            raise ValueError("The name must be longer than 4 characters.")
        
        return value
    
    @field_validator("price")
    def validate_price(cls,value: float) -> float:
        if value <= 0:
            raise ValueError("The price mush be greather than 0")
        return value
    
    @field_validator("type_id")
    def validate_type(cls,value: int) -> int:
        if value <= 0:
            raise ValueError("The type_id must be greather than 0")
        return value
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "name": "Coca Cola",
                    "description":"Chop Suey",
                    "price": 2.45,
                    "type_id": 1,
                    "status": True
                }
            }
    }


class DishUpdate(DishRequest):
    name: str = None
    description: str = None
    price: float = None
    type_id: int = None