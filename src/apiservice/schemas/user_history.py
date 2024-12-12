from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
import uuid


class UserHistoryBase(BaseModel):
    user_id: uuid.UUID
    details: Optional[Dict] = None


class UserHistoryCreate(UserHistoryBase):
    recommendation_id: Optional[uuid.UUID] = None
    recommendation_data: Optional[Dict] = None


class UserHistoryResponse(UserHistoryBase):
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    recommendation_id: Optional[uuid.UUID] = None
    recommendation_data: Optional[Dict] = None

    class Config:
        orm_mode = True
