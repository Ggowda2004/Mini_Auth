from app.db.base import Base
import uuid
from datetime import datetime,timezone
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.db.models.audit_log import AuditLogs


class APIKey(Base):
    __tablename__="api_keys"
    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name:Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    key_hash:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )

    revoked:Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )

    expires_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    last_used_at:Mapped[datetime | None]=mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    user=relationship(
        "User",
        back_populates="api_keys",
    )

    audit_logs: Mapped[list["AuditLogs"]] = relationship(
    back_populates="api_key",
    cascade="all, delete-orphan"
    )

# CREATE TABLE api_keys 
#     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

#     user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

#     name VARCHAR(100) NOT NULL,
#     key_hash TEXT NOT NULL,

#     revoked BOOLEAN DEFAULT FALSE,

#     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
#     last_used_at TIMESTAMP WITH TIME ZONE
# )