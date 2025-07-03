from pydantic import BaseModel,field_validator

class CurrencyResponse(BaseModel):
    id: int
    name: str
    exchange: float
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": "1",
                    "name": "Bolivar",
                    "exchange": 103.97
                }
            }
    }
    

class CurrencyRequest(BaseModel):
    name: str
    exchange: float
    
    @field_validator("name")
    def validate_name(cls,value:str):
        value = value.upper()
        if len(value) < 2:
            raise ValueError("Name must have 4 or more characters.")
        return value


    @field_validator("exchange")
    def validate_exchange(cls,value:float):
        if value < 0:
            raise ValueError("The exchange must be greater than 0.")
        
        return value

    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "name": "Bolivar",
                    "exchange": 103.97
                }
            }
    }
    

class CurrencyUpdate(CurrencyRequest):
    name: str = None
    exchange: float = None