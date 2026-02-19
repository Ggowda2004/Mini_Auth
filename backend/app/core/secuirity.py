import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.exceptions import AuthError
from .config import Settings


#1 task to hash and verify password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
def hash_password(password:str):
    return bcrypt_context.hash(password)

def verify_password(plain_password:str, hash_pass:str):
    return bcrypt_context.verify(plain_password,hash_pass)
# hash_password()
# verify_password()

#2 create tokens
ALGORITHM=Settings.jwt_algorithm

def create_access_token(data:dict):
    to_encode=data.copy()
    expiry=datetime.now(timezone.utc) + timedelta(minutes=Settings.access_token_expiry_minutes)
    to_encode.update({"exp":expiry})
    return jwt.encode(payload=to_encode,key=Settings.jwt_secret_key,algorithm=ALGORITHM)

def verify_access_token(token):
    try:
        payload=jwt.decode(token,key=Settings.jwt_secret_key,algorithms=[ALGORITHM])
        return payload#decode automatically verifies expiry time
    except ExpiredSignatureError:
        raise  AuthError("The token is expired")
    except JWTError:
        raise AuthError("The token is invalid")
    
# create_access_token()
# verify_access_token()

api_key_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_api_key(api_key:str):
    return api_key_context.hash(api_key)
def verify_api_key(api_key:str,hash_key:str):
    return api_key_context.verify(api_key,hash_key)


# hash_api_key()
# verify_api_key()