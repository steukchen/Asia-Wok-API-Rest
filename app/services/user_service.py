from app.db.repositories import UserRepository
from app.schemas.user import UserResponse

class UserService:
    def __init__(self):
        self.repo = UserRepository()
    
    def get_user_by_username(self,username:str) -> UserResponse:
        user_db = self.repo.get_user_by_username(username=username)
        if not user_db:
            return None
        user_response = UserResponse(
            id=str(user_db.id),
            username=user_db.username,
            email=user_db.email,
            rol=user_db.rol
        )
        return user_response
        