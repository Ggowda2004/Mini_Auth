from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.exceptions import AuthError
from .config import settings
import hashlib

#1 task to hash and verify password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
def hash_password(password:str):
    return bcrypt_context.hash(password)

def verify_password(plain_password:str, hash_pass:str):
    return bcrypt_context.verify(plain_password,hash_pass)
# hash_password()
# verify_password()

#2 create tokens
ALGORITHM=settings.jwt_algorithm

def create_access_token(data:dict):
    to_encode=data.copy()
    expiry=datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expiry_minutes)
    to_encode.update({"exp":expiry})
    return jwt.encode(to_encode,settings.jwt_secret_key,ALGORITHM)

def verify_access_token(token):
    try:
        payload=jwt.decode(token,settings.jwt_secret_key,[ALGORITHM])
        return payload#decode automatically verifies expiry time
    except ExpiredSignatureError:
        raise  AuthError("The token is expired")
    except JWTError:
        raise AuthError("The token is invalid")
    
# create_access_token()
# verify_access_token()

def hash_api_key(raw_key:str)->str:
    return hashlib.sha256(raw_key.encode()).hexdigest()
"""
    Hashes a raw API key using SHA-256. 
    Deterministic: Same input always results in the same output.
"""

# hash_api_key()
# verify_api_key()