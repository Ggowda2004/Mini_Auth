#security → no FastAPI dependency so no error raised, rather we define custom error and define custom functions to handle security related tasks in middleware and routers
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.exceptions import AuthError

#1 task to hash and verify password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
def hash_password(password:str):
    return bcrypt_context.hash(password)

def verify_password(plain_password:str, hash_pass:str):
    return bcrypt_context.verify(plain_password,hash_pass)
# hash_password()
# verify_password()

#2 create tokens
"""first user logs in, immediatley the server starts working on generating the token 
1-> gathers required payload (all minimal data ->user id, role, expiry)
2-> header is prepared by server based on the hasing used(by server)
3-> both payload and header are encoded and joinned using a dot(by server)
4-> a secret key is used and a choosen algorithm is performed to finally add a signature(before) structure qqqqqqqqq.ddddddddd.rrrrrrrrrr"""
'''
CREATE TOKEN
→ encode(payload + secret)

VERIFY TOKEN
→ decode(token + same secret)
→ if valid → get payload
'''

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"

def create_access_token(data:dict):
    to_encode=data.copy()
    expiry=datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp":expiry})
    return jwt.encode(payload=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token):
    try:
        payload=jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
        return payload#decode automatically verifies expiry time
    except ExpiredSignatureError:
        raise  AuthError("The token is expired")
    except JWTError:
        raise AuthError("The token is invalid")
    
# create_access_token()
# verify_access_token()

# hash_api_key()
# verify_api_key()