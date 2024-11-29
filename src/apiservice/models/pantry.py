from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    JSONB,
    func,
)
from sqlalchemy.orm import relationship
from models.database import Base


class PantryItems(Base):
    __tablename__ = "pantry"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    items = Column(JSONB, nullable=False, default=lambda: {})
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="pantry")

    def __repr__(self):
        return f"<PantryItems(user_id={self.user_id})>"
