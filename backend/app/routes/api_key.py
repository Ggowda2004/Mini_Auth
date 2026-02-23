# POST /api-keys → create key (protected -> means the current_user is authenticated using get_current_user)
# GET /api-keys → list keys
# DELETE /api-keys/{id} → revoke key


from fastapi import APIRouter, status, Depends, HTTPException
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.db.models.user import User
from app.schemas.api_key import MakeAPIKey
from app.db.models.api_keys import APIKey
from app.services.api_key_service import store_api_key, revoke_api_key
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid
from app.core.exceptions import AuthError

router1=APIRouter(
    prefix="/api-keys",
    tags=["Api_key_usage"]
)

@router1.post("/",status_code=status.HTTP_201_CREATED)
def create_key(api_name:MakeAPIKey,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    user_id=current_user.id
    key_details=store_api_key(db,api_name,user_id)
    return key_details

@router1.get("/",status_code=status.HTTP_200_OK)
def list_keys(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    key=select(APIKey).where(APIKey.user_id==current_user.id)
    api_keys=db.scalars(key).all()
    if not api_keys:
        return []
    return api_keys


@router1.delete("/{key_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_key(key_id:uuid.UUID,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    try:
        return revoke_api_key(db,key_id,current_user.id)
    except AuthError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)