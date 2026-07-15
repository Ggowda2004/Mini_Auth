from app.schemas.users import CreateUser
from app.schemas.login_user import LoginUser
from app.core.exceptions import AuthError
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token

def auth_service_register_user(db:Session,user_data:CreateUser):
    email = user_data.email
    existing_user = db.query(User).filter_by(email=email).first()
    if existing_user:
        raise AuthError("Email is already registered")

    password=user_data.password
    hashed_password=hash_password(password)

    new_user=User(
        email=email,
        hashed_password=hashed_password,
    )

    try:
        db.add(new_user)   #→ put in session (not saved)
        db.commit()         #→ write to database
    except Exception:
        db.rollback()
        raise

    db.refresh(new_user)    #→ get DB-generated values (id, timestamps)
    return new_user


#------------------------------------------------------------------------------------



def auth_service_login_user(db:Session,user_data:LoginUser):
    email=user_data.email
    password=user_data.password
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise AuthError("Invalid credentials")
    if not verify_password(password,user.hashed_password):
        raise AuthError("Invalid credentials")
    if not user.is_active:
        raise AuthError("Account is deactivated. Please contact support.")
    payload={
        "sub":str(user.id),
        "role": "admin" if user.is_superuser else "user"
             }
    access_token = create_access_token(data=payload)
    refresh_token = create_refresh_token(data=payload)
    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
        }


#-------------------------------------------------------------------------------------

#logout
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone
from app.core.config import settings
import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
ALGORITHM = settings.jwt_algorithm

def auth_service_logout_user(access_token: str, refresh_token: str):
    try:
        now = datetime.now(timezone.utc).timestamp()
        access_payload = jwt.decode(access_token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        access_jti = access_payload.get("jti")
        access_exp = access_payload.get("exp")
        
        if access_jti and access_exp:
            access_ttl = int(access_exp - now)
            if access_ttl > 0:
                redis_client.setex(name=f"blacklist:{access_jti}", time=access_ttl, value="true")
        
        refresh_payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        refresh_jti = refresh_payload.get("jti")
        refresh_exp = refresh_payload.get("exp")
        
        if refresh_jti and refresh_exp:
            refresh_ttl = int(refresh_exp - now)
            if refresh_ttl > 0:
                redis_client.setex(name=f"blacklist:{refresh_jti}", time=refresh_ttl, value="true")
    except JWTError:
        raise AuthError("Could not process token payload")
    

#--------------------------------------------------------------------------------------
#refresh token
def auth_service_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[ALGORITHM])

        refresh_jti = payload.get("jti")
        if refresh_jti and redis_client.get(f"blacklist:{refresh_jti}"):
            raise AuthError("This refresh token has been revoked via logout")

        if payload.get("type") != "refresh":
            raise AuthError("Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise AuthError("Invalid token payload")
        new_access_token = create_access_token({"sub": user_id})

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except (JWTError, ExpiredSignatureError):
        raise AuthError("Refresh token expired, please login again or token invalid")

