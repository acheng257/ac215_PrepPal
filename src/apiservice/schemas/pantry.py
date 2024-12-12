from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from uuid import UUID
from datetime import datetime


class PantryBase(BaseModel):
    items: Dict[str, int] = Field(default_factory=dict, example={"apples": 5, "bread": 2})


class PantryCreate(PantryBase):
    pass


class PantryUpdate(BaseModel):
    items: Optional[Dict[str, int]] = None
    ingredients: Optional[List[str]] = None


class PantryResponse(PantryBase):
    user_id: UUID
    last_updated: datetime

    class Config:
        orm_mode = True
