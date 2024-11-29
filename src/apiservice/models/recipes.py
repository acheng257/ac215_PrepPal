from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID, TEXT
from sqlalchemy.orm import relationship
from models.database import Base
import uuid


class Recipes(Base):
    __tablename__ = "recipes"

    recipe_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instructions = Column(TEXT)
    ingredients = Column(TEXT)
    cooking_time = Column(Integer)
    calories = Column(Integer)
    protein = Column(Integer)

    favorited_by = relationship("UserPreferences", back_populates="favorite_recipes")

    def __repr__(self):
        return f"<Recipes(user_id={self.user_id})>"
