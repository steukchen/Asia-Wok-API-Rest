from fastapi import APIRouter,status,Path,HTTPException,Depends
from fastapi.responses import JSONResponse
from app.schemas.user import UserResponse,UserRequest,UserUpdate
from app.services import UserService

router = APIRouter()

@router.get("/get_users",status_code=status.HTTP_200_OK)
def get_users(service: UserService = Depends()):
    users_response = service.get_all()
    
    if not users_response:
        raise HTTPException(detail="Users not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=[user_response.model_dump() for user_response in users_response],status_code=status.HTTP_200_OK)


@router.get("/get_user_by_username/{username}",status_code=status.HTTP_200_OK)
def get_user_by_username(username: str = Path(min_length=5), service: UserService = Depends()) -> UserResponse:
    username = username.upper()
    user_response = service.get_one_by_column(column="username",value=username)
    
    if not user_response:
        raise HTTPException(detail="User not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=user_response.model_dump(),status_code=status.HTTP_200_OK)

@router.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user(user_request: UserRequest,service: UserService = Depends()):
    user = service.create_one(item_request=user_request)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not Created")
    return JSONResponse(user.model_dump(),status_code=status.HTTP_201_CREATED)

@router.put("/update_user/{id}",status_code=status.HTTP_200_OK)
def update_user(user_update: UserUpdate,id: str = Path(min_length=10),service: UserService = Depends()):
    user = service.update_one_by_column_primary(value=id,item_update=user_update)
    if not user:
        raise HTTPException(detail="User not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(user.model_dump(),status_code=status.HTTP_200_OK)

@router.delete("/delete_user/{id}",status_code=status.HTTP_200_OK)
def delete_user(id: str = Path(), service: UserService = Depends()):
    is_user_deleted = service.delete_one(value=id)
    
    if not is_user_deleted:
        raise HTTPException(detail="User not found",status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content="User deleted",status_code=status.HTTP_200_OK)