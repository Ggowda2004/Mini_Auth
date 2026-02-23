from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session

from app.core.security import verify_access_token
from app.core.exceptions import AuthError
from app.db.models.user import User
from app.db.session import get_db

# 1. Define Security Schemes (This makes the Green Lock/Authorize button appear)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth_f/v1/auth/login", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def validate_token(token: str, db: Session):
    try:
        payload = verify_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise AuthError("No user ID in token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AuthError("User not found")
        return user
    except Exception:
        raise AuthError("Invalid or expired JWT")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),   # FastAPI automatically looks for 'Authorization: Bearer ...'
    api_key: str = Depends(api_key_header) # FastAPI automatically looks for 'x-api-key' in headers
):
    # Check JWT Token first
    if token:
        return validate_token(token, db)
    
    # Check API Key second
    if api_key:
        from app.services.api_key_service import validate_api_key
        user = validate_api_key(db, api_key)
        if not user:
            raise AuthError("Invalid API key")
        return user
    
    # Neither provided
    raise AuthError("No authentication credentials provided")
