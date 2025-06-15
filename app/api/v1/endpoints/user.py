from fastapi import APIRouter,status,Path
from fastapi.responses import JSONResponse
from app.schemas.user import UserResponse,UserRequest,UserUpdate
from app.services import UserService

router = APIRouter()

@router.get("/get_user_by_username/{username}",status_code=status.HTTP_200_OK)
def get_user_by_username(username: str = Path(min_length=3)) -> UserResponse:
    username = username.upper()
    service = UserService()
    user_response = service.get_user_by_username(username)
    
    if not user_response:
        return JSONResponse(content=f"{username} not Found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=user_response.model_dump(),status_code=status.HTTP_200_OK)

@router.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user(user_request: UserRequest):
    service = UserService()
    user = service.create_user(user_request=user_request)
    
    if not user:
        return JSONResponse("Username or Email already in use",status_code=status.HTTP_409_CONFLICT)
    
    return JSONResponse(user.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_user/{username}",status_code=status.HTTP_200_OK)
def update_user(user_update: UserUpdate,username: str = Path()):
    service = UserService()

    user = service.update_user(username=username,user_update=user_update)
    
    if not user:
        return JSONResponse("Username not Updated",status_code=status.HTTP_409_CONFLICT)
    
    return JSONResponse(user.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_user/{username}",status_code=status.HTTP_200_OK)
def delete_user(username: str = Path()):
    service = UserService()
    
    user_deleted = service.delete_user(username=username)
    
    if not user_deleted:
        return JSONResponse("User not deleted",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content="User deleted",status_code=status.HTTP_200_OK)