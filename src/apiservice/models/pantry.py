# models/pantry.py

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    # JSONB,
    JSON,
    func,
)
from sqlalchemy.orm import relationship
from models.database import Base


class PantryItem(Base):
    __tablename__ = "pantry"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    items = Column(JSON, nullable=False, default=lambda: {})
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="pantry_items")

    def __repr__(self):
        return f"<PantryItem(user_id={self.user_id})>"
