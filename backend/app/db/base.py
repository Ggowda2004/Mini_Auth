from sqlalchemy.ext.declarative import declarative_base

class Base(declarative_base):
    pass

from app.db.models.user import User
from backend.app.db.models.api_keys import ApiKey
from app.db.models.audit_log import AuditLog

#Import all models here so Alembic can discover them, otherwise, it won't be able to generate migrations for them.
#check out alembic***