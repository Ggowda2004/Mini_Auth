# POST   /auth/register
# POST   /auth/login
# GET    /auth/me
# Route should NOT talk to DB directly.
# In FastAPI, if you return an error object, the API will still send a 200 OK status code to the client, which is misleading. You must use raise HTTPException so the browser/frontend knows something went wrong (e.g., a 400 Bad Request).
"""AuthError should NOT be raised in routes

You wrote:

raise AuthError(...)
Problem:

AuthError is your internal service exception

Routes should return HTTP responses

FastAPI won’t automatically convert your custom error properly (unless you added handler)
route layer → HTTP handling
service layer → business errors"""
# Use response_model (later — you said already)

from fastapi import APIRouter, status, Depends, HTTPException
from app.services.auth_service import auth_service_register_user, auth_service_login_user
from app.schemas.users import CreateUser
from app.db.models.user import User
from app.core.exceptions import AuthError
from app.schemas.login_user import LoginUser
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",summary="Register the user",status_code=status.HTTP_200_OK)
def register_user(user_data:CreateUser,db:Session=Depends(get_db)):
    try:
        new_user=auth_service_register_user(db,user_data)
        return {
            "message":"User registered successfully",
            "user_id":new_user.id,
            "email": new_user.email
            }
    except AuthError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")


@router.post("/login",status_code=status.HTTP_200_OK)
def login_user(user_data:LoginUser, db:Session=Depends(get_db)):
    try:
        token=auth_service_login_user(db,user_data)
        return token
    except AuthError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    

@router.get("/me",status_code=status.HTTP_200_OK)
def verify_me(current_user:User = Depends(get_current_user)):
    '''What happens: When a request hits this route, FastAPI automatically runs your get_current_user logic. If the token is invalid, it throws an error before even touching your function code.'''
    return {
        "user_id":current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "role":current_user.is_superuser
    }

# Auth system complete → build API key routes