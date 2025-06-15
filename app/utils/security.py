from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def hash_password(password:str) -> str:
    ph = PasswordHasher()
    hash = ph.hash(password)
    return hash
    
def validate_password(password: str, hash: str) -> bool:
    ph = PasswordHasher()
    try:
        ph.verify(hash=hash,password=password)
        return True
    except VerifyMismatchError:
        return False