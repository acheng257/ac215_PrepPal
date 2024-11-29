# models/users.py

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    ARRAY,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.orm import relationship
from models.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(200), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    pantry_items = relationship("PantryItem", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, first_name='{self.first_name}', last_name='{self.last_name}')>"


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    recipe_history = Column(ARRAY(UUID(as_uuid=True)), default=[])
    allergies = Column(ARRAY(TEXT), default=[])
    favorite_cuisines = Column(ARRAY(TEXT), default=[])
    favorite_recipes = Column(ARRAY(UUID(as_uuid=True)), default=[])
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreferences(user_id={self.user_id})>"
