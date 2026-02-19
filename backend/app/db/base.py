from sqlalchemy.ext.declarative import declarative_base

class Base(declarative_base):
    pass

from app.db.models.user import User
from backend.app.db.models.api_keys import APIKey
from app.db.models.audit_log import AuditLogs