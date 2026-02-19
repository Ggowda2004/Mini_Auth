from app.db.base import Base
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.db.models.api_keys import APIKey
    from app.db.models.audit_log import AuditLogs
class User(Base):
    __tablename__="users"
    id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid = True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    email:Mapped[str]=mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )

    is_active:Mapped[bool]=mapped_column(
        Boolean,
        default=True
    )

    is_superuser:Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    #mentioning relationship

    api_keys:Mapped[list["APIKey"]]=relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    audit_logs: Mapped[list["AuditLogs"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan"
    )