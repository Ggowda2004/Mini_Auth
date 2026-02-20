from app.schemas.users import CreateUser
from app.schemas.login_user import LoginUser
from app.core.exceptions import AuthError
from app.db.models.user import User
from sqlalchemy.orm import Session
from backend.app.core.security import hash_password, verify_password, create_access_token

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
    return {
        "access_token":access_token,
        "token_type":"bearer"
        }


#-------------------------------------------------------------------------------------




