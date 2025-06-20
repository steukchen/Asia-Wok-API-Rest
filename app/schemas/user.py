from pydantic import BaseModel,field_validator
from app.utils import validate_email,hash_password

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    rol: str
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": 1,
                    "username": "HARSUE",
                    "email": "HARSUE0311@GMAIL.COM",
                    "rol": "superadmin"
                }
            }
    }
    
class UserRequest(BaseModel):
    username: str
    email: str
    rol: str = "waiter"
    password: str
    
    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        value =value.upper()
        
        if len(value) <= 4:
            raise ValueError("The username must be longer than 4 characters.")
        
        return value
    
    @field_validator("rol")
    def validate_rol(cls,value: str) -> str:
        roles = ["waiter","chef",'admin','superadmin']
        value = value.lower()
        if value not in roles:
            raise ValueError("Invalid Rol.")
        
        return value
    
    @field_validator("email")
    def validate_email(cls,value: str) -> str:
        value = value.upper() 
        
        if not validate_email(value):
            raise ValueError("Invalid Email.")
        
        return value
    
    @field_validator("password")
    def validate_password(cls,value: str) -> str:
        return hash_password(value)
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "username": "HARSUE",
                    "email": "HARSUE0311@GMAIL.COM",
                    "rol": "superadmin",
                    "password": "fakepassword123"
                }
            }
    }
        
        
class UserUpdate(UserRequest):
    username: str = None
    email: str = None
    rol: str = None
    password: str = None
    