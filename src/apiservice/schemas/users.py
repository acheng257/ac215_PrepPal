from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    phone_number: str = Field(..., max_length=20)


class UserPreferencesBase(BaseModel):
    recipe_history: Optional[List[UUID]] = []
    allergies: Optional[List[str]] = []
    favorite_cuisines: Optional[List[str]] = []
    favorite_recipes: Optional[List[UUID]] = []


class UserCreate(UserBase):
    user_preferences: UserPreferencesBase


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)


class UserResponse(UserBase):
    user_id: UUID
    registration_date: datetime
    last_updated: datetime

    class Config:
        orm_mode = True


# class UserPreferencesCreate(UserPreferencesBase):
#     pass


class UserPreferencesUpdate(BaseModel):
    recipe_history: Optional[List[UUID]] = None
    allergies: Optional[List[str]] = None
    favorite_cuisines: Optional[List[str]] = None
    favorite_recipes: Optional[List[UUID]] = None


class UserPreferencesResponse(UserPreferencesBase):
    user_id: UUID
    last_updated: datetime

    class Config:
        orm_mode = True
