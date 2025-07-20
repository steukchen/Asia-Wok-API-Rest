from pydantic import BaseModel,field_validator
from app.utils import validate_email,hash_password
from re import fullmatch

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    rol: str
    status: bool
    
    @field_validator("id",mode="before")
    def validate_id(cls,value):
        return str(value)

    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "id": "76ff5576-f9c2-4b85-844e-dff1b3b9a3dd",
                    "username": "HARSUE",
                    "email": "HARSUE0311@GMAIL.COM",
                    "rol": "admin"
                }
            }
    }

class UserDataResponse(BaseModel):
    user_data: UserResponse
    ws_token: str

class UserRequest(BaseModel):
    username: str
    email: str
    rol: str = "waiter"
    status: bool = True
    password: str
    
    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        value =value.upper()
        if " " in value:
            raise ValueError("The username cannot have spaces.")
        if len(value) <= 3:
            raise ValueError("The username must be longer than 3 characters.")
        
        return value
    
    @field_validator("rol")
    def validate_rol(cls,value: str) -> str:
        roles = ['admin','cashier','chef','waiter']
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
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$'
        if not fullmatch(regex, value):
            raise ValueError(
                "Password must have at least one number, one special character, one uppercase letter, one lowercase letter, and be at least 8 characters long"
            )
        
        return hash_password(value)
    
    model_config = {
        "json_schema_extra":
            {
                "example": {
                    "username": "HARSUE",
                    "email": "HARSUE0311@GMAIL.COM",
                    "rol": "admin",
                    "password": "FakePassword123.",
                    "status": True
                }
            }
    }
        
        
class UserUpdate(UserRequest):
    username: str = None
    email: str = None
    rol: str = None
    password: str = None
    