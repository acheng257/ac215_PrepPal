# from sqlalchemy import (
#     Column,
#     Integer,
# )
# from sqlalchemy.dialects.postgresql import UUID, TEXT
# from sqlalchemy.orm import relationship
# from models.database import Base
# import uuid


# class Recipes(Base):
#     __tablename__ = "recipes"

#     recipe_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     instructions = Column(TEXT)
#     ingredients = Column(TEXT)
#     cooking_time = Column(Integer)
#     calories = Column(Integer)
#     protein = Column(Integer)

#     favorited_by = relationship("UserPreferences", back_populates="favorite_recipes")

#     def __repr__(self):
#         return f"<Recipes(user_id={self.user_id})>"
# models/recipes.py

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.orm import relationship
from models.database import Base
import uuid


class Recipes(Base):
    __tablename__ = "recipes"

    recipe_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), unique=True, nullable=False)
    instructions = Column(TEXT, nullable=False)
    ingredients = Column(TEXT, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="recipes")

    def __repr__(self):
        return f"<Recipe(title={self.title}, user_id={self.user_id})>"
