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
"""this is to avoid circular imports. If we import APIKey at the top, it will also try to import
User, which will lead to an infinite loop. By using TYPE_CHECKING, we can tell the type checker to
ignore this import at runtime, but still allow us to use APIKey in our type hints"""

#Column (Legacy): The old way (1.x). It doesn't understand Python type hints. Your IDE won't know if user.id is an integer or a string unless you tell it twice.
#mapped_column (Modern): The new way (2.0+). It is designed to work with the Mapped[] type hint. It "reads" the Python type and automatically configures the database column for you.
class User(Base):
    __tablename__="users"
    # id: Mapped[uuid.UUID] ensures type safety in Python
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

# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

# CREATE TABLE users (
#     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
#     email VARCHAR(255) UNIQUE NOT NULL,
#     hashed_password TEXT NOT NULL,
    
#     is_active BOOLEAN DEFAULT TRUE,
#     is_superuser BOOLEAN DEFAULT FALSE,

#     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
#     updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
# );
