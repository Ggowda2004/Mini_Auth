import secrets
from app.schemas.api_key import MakeAPIKey
from app.core.security import hash_api_key
from sqlalchemy.orm import Session
from app.db.models.api_keys import APIKey
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from app.core.exceptions import AuthError
import uuid


def generate_api_key():
    raw_key_without_prefix=secrets.token_urlsafe(32)
    raw_key=f"sk_live_{raw_key_without_prefix}"
    return raw_key


def store_api_key(db:Session,api_name:MakeAPIKey,current_user:uuid.UUID):
    name= api_name.name
    raw_key=generate_api_key()
    hashed_key = hash_api_key(raw_key)
    expiry_api_key= datetime.now(timezone.utc) + timedelta(days=settings.api_key_expiry)
    new_key=APIKey(
        user_id=current_user,
        name=name,
        key_hash=hashed_key,
        expires_at=expiry_api_key
        )
    try:
        db.add(new_key)
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(new_key)
    return {
        "key_id":new_key.id,
        "key_name":new_key.name,
        "raw_key":raw_key,
        "expiry":new_key.expires_at
    }
#------------------------------------------------------------------------------

def revoke_api_key(db:Session,key_id:uuid.UUID,user_id:uuid.UUID):
    key_record=db.query(APIKey).filter_by(id=key_id,user_id=user_id).first()
    if not key_record:
        raise AuthError("no key found")
    if key_record.revoked:
        return f"user_id{user_id} key already revoked"
    key_record.revoked = True
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(key_record)
    return f"user_id{user_id} key revoked"

#-------------------------------------------------------------------------------

def validate_api_key(db:Session,raw_key:str):
    if not raw_key.startswith("sk_live_"):
        raise AuthError("Invalid Key or No key match found") #Invalid Key"
    hashed_key=hash_api_key(raw_key)
    key_record=db.query(APIKey).filter_by(key_hash=hashed_key).first() #------------------------------------------
    current_date_time=datetime.now(timezone.utc)
    if not key_record:
        raise AuthError("Invalid Key or No key match found")  #Invalid Key"
    if key_record.expires_at and key_record.expires_at < current_date_time:
        raise AuthError("Invalid Key or No key match found") #The key is expired"
    if key_record.revoked:
        raise AuthError("Invalid Key or No key match found")   #key is revoked"
    return key_record.user