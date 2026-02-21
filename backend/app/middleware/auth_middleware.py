from fastapi import Request, Depends #Only Request gives access to headers.
from app.core.security import verify_access_token
from app.core.exceptions import AuthError
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.services.api_key_service import validate_api_key
from app.db.session import get_db

def validate_token(token:str,db:Session):
    try:
        payload=verify_access_token(token)
        user_id=payload.get("sub")

        if not user_id:
            raise AuthError("No user found")
        user=db.query(User).filter_by(id=user_id).first()
        if not user:
            raise AuthError("No user found")
        return user
    except Exception as e:
        raise AuthError("unexpected JWT error")
    
def validate_key(db:Session,api_key:str):
    user= validate_api_key(db,api_key)
    if not user:
        raise AuthError("Invalid API key")
    return user

#Request → class ❌
# request → instance ✅
def get_current_user(request:Request, db:Session = Depends(get_db)):
    
    auth_header=request.headers.get("Authorization")
    api_key=request.headers.get("x-api-key")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        return validate_token(token, db)
    
    if api_key:
        return validate_key(db, api_key )
    
    if not api_key and not auth_header:
        raise AuthError("No authentication credentials provided")
    
    raise AuthError("No valid authentication credentials provided")

