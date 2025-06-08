from fastapi import APIRouter,status,Path
from fastapi.responses import JSONResponse
from app.schemas.user import UserResponse
from app.services import UserService

router = APIRouter()

@router.get("get_user/{username}",status_code=status.HTTP_200_OK)
def get_user(username: str = Path(min_length=3)) -> UserResponse:
    username = username.upper()
    service = UserService()
    user_response = service.get_user_by_username(username)
    
    if not user_response:
        return JSONResponse(content=f"{username} not Found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=user_response.model_dump(),status_code=status.HTTP_200_OK)