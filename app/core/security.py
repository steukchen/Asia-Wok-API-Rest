from jose import jwt
from fastapi import HTTPException,status,Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError,ExpiredSignatureError
import json
from datetime import datetime,UTC,timedelta
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(settings.API_V1_STR+"/token")

def encode_token(id:str,rol:str,ws=False):
    try:
        time = timedelta(days=7) if not ws else timedelta(minutes=30)
        payload = {
            "sub": json.dumps(
                    {
                        "id":id,
                        "rol": rol
                    }),
            "exp": datetime.now(UTC) + time
        }
        token = jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
        return token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def verify_token(token: str):
    try:
        payload = jwt.decode(token=token,algorithms=settings.ALGORITHM,key=settings.SECRET_KEY)
        sub = payload["sub"]
        return sub
    except ExpiredSignatureError:
        raise HTTPException(detail="TOKEN HAS EXPIRED",status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(detail="TOKEN IS INVALID",status_code=status.HTTP_401_UNAUTHORIZED)


def validate_token(token:str) -> dict | None:
    data = json.loads(verify_token(token))
    return data


def get_data_token(access_token: str = Depends(oauth2_scheme)):
    data = validate_token(token=access_token)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token"
            )
    
    return data
    
token_depend = Annotated[dict,Depends(get_data_token)]
