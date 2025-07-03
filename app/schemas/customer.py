from pydantic import BaseModel,field_validator
from re import match

class CustomerResponse(BaseModel):
    id: int
    ci: str
    name: str
    lastname: str
    phone_number: str
    address: str | None = None
    

    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": "1",
                    "ci": "V-32322998",
                    "name": "Pedro",
                    "lastname": "Perez",
                    "phone_number": "416177829",
                    "address": "Calle 7 Cordero"
                }
            }
    }
    

class CustomerRequest(BaseModel):
    ci: str
    name: str
    lastname: str
    phone_number: str
    address: str | None = None
    
    @field_validator("ci")
    def validate_ci(cls,value:str):
        value = value.upper()
        regex = r"^[A-Z]-\d{7,8}$"
        if not bool(match(regex,value)):
            raise ValueError("The CI does not comply with the appropriate format")
        return value
    
    @field_validator("name","lastname")
    def validate_name(cls,value:str):
        print(cls)
        return value

    @field_validator("phone_number")
    def validate_phone_number(cls,value:str):
        regex = r"^(?:\+\d{1,3}\s?)?(?:[\d\s\-\.]{7,14}\d)$"
        if not bool(match(regex,value)):
            raise ValueError("Phone number Invalid")
        
        return value

    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "ci": "V-32322998",
                    "name": "Pedro",
                    "lastname": "Perez",
                    "phone_number": "416177829",
                    "address": "Calle 7 Cordero"
                }
            }
    }
    

class CustomerUpdate(CustomerRequest):
    ci: str = None
    name: str = None
    lastname: str = None
    phone_number: str = None
    address: str | None = None