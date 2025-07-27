from fastapi import APIRouter,Form,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from app.core.security import encode_token,token_depend
from app.services import UserService
from app.schemas.user import UserDataResponse

router = APIRouter()

class RequestForm:
    def __init__(self,username: str = Form(...), password: str = Form(...)):
        self.username = username.upper()
        self.password = password

@router.post("/token")
def login(form_data: RequestForm = Depends(), service: UserService = Depends()) -> JSONResponse:
    user = service.validate_user(username=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID CREDENTIALS",
            )
    token = encode_token(user["id"],user["rol"])
    response = JSONResponse(content={"access_token": token, "token_type": "bearer"},status_code=status.HTTP_200_OK)
    
    return response

@router.get("/validate_token",status_code=status.HTTP_200_OK)
def get_validate_token(data: token_depend,service: UserService = Depends()) -> UserDataResponse:
    user = service.get_one_by_column_primary(value=data["id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="INVALID CREDENTIALS")

    ws_token = encode_token(id=data["id"],rol=data["rol"],ws=True)
    
    return UserDataResponse(user_data=user,ws_token=ws_token)

