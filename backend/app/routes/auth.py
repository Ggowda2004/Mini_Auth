from fastapi import APIRouter, status, Depends, HTTPException, Request, Response
from app.services.auth_service import auth_service_register_user, auth_service_login_user, auth_service_logout_user, auth_service_refresh_token
from app.schemas.users import CreateUser
from app.db.models.user import User
from app.core.exceptions import AuthError
from app.schemas.login_user import LoginUser
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import TokenRefreshRequest, LogoutRequest
from fastapi.responses import JSONResponse

router2=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router2.post("/register",summary="Register the user",status_code=status.HTTP_200_OK)
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


@router2.post("/login",status_code=status.HTTP_200_OK)
def login_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    try:
        user_data=LoginUser(email=form_data.username,password=form_data.password)
        token_data=auth_service_login_user(db,user_data)
        # return token_data
        response = JSONResponse(
            content={
                "access_token": token_data["access_token"],
                "token_type": token_data["token_type"],
            }
        )

        response.set_cookie(
            key="refresh_token",
            value=token_data["refresh_token"],
            httponly=True,
            secure=False,   # set True in production with HTTPS
            samesite="lax",
            path="/",
            max_age=7 * 24 * 60 * 60,
        )

        return response
    except AuthError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    

@router2.get("/me")
def verify_me(current_user:User = Depends(get_current_user)):
    '''What happens: When a request hits this route, FastAPI automatically runs your get_current_user logic. If the token is invalid, it throws an error before even touching your function code.'''
    return {
        "user_id":current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "role":current_user.is_superuser
    }

# Auth system complete → build API key routes

@router2.post("/logout", status_code=status.HTTP_200_OK, summary="Logout User")
def logout_user(request: Request, response: Response, token: str = Depends(oauth2_scheme)):
    """
    Extracts the token from the request authorization headers, 
    passes it down to the business logic layer to blacklist it, 
    and handles route layer HTTP exceptions.
    """
    refresh_token = request.cookies.get("refresh_token")

    try:
        auth_service_logout_user(access_token=token, refresh_token=refresh_token)
        response.delete_cookie("refresh_token", path="/")
        return {"detail": "Successfully logged out and session revoked"}
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    

# refresh token
@router2.post("/refresh", status_code=status.HTTP_200_OK, summary="Refresh Access Token")
def refresh_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token provided")


    try:
        result = auth_service_refresh_token(refresh_token)
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=False,   # True in production / samesite=None
            samesite="lax", #lax-mid, None-pro, strict-low (ability to aloow cross site)
            path="/",
            max_age=7 * 24 * 60 * 60,
        )
        return {
            "access_token": result["access_token"],
            "token_type": result["token_type"],
        }

    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))