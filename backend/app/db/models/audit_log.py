from app.db.base import Base
from sqlalchemy import String, Text, ForeignKey, DateTime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
class AuditLogs(Base):
    __tablename__="audit_logs"
    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="SET NULL"),
        #when parent is deleted → child column becomes NULL as i have set ondelete
        nullable=True
    )

    api_key_id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("api_keys.id",ondelete="SET NULL"),
        nullable=True
    )
    
    event_type:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )

    ip_address:Mapped[str]=mapped_column(
        String
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc)
    )

    user=relationship("User", back_populates="audit_logs")
    api_key=relationship("APIKey", back_populates="audit_logs")
