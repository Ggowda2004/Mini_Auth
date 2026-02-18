from app.db.base import Base
from sqlalchemy import String, Text, ForeignKey, DateTime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
"""uuid4 Completely random number
No relation to input data
Collision chance extremely low
auto_increment in simple not scalable for mutilple servers or table(conflict)
uuid is random min conflict ex:128 bits = 16 bytes = 32 hexadecimal characters550e8400-e29b-41d4-a716-446655440000"""

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
        #when parent is deleted → child column becomes NULL)
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
# CREATE TABLE audit_logs (
#     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

#     user_id UUID REFERENCES users(id) ON DELETE SET NULL,
#     api_key_id UUID REFERENCES api_keys(id) ON DELETE SET NULL,

#     event_type VARCHAR(100) NOT NULL,
#     ip_address VARCHAR(45),

#     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
# );
