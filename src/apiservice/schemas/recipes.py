from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class RecipeBase(BaseModel):
    instructions: Optional[str] = Field(None, example="Mix ingredients and cook for 20 minutes.")
    ingredients: Optional[str] = Field(None, example="Flour, Eggs, Milk")
    cooking_time: Optional[int] = Field(None, ge=0, example=20)  # in minutes
    calories: Optional[int] = Field(None, ge=0, example=500)
    protein: Optional[int] = Field(None, ge=0, example=25)  # in grams


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    instructions: Optional[str] = None
    ingredients: Optional[str] = None
    cooking_time: Optional[int] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    protein: Optional[int] = Field(None, ge=0)


class RecipeResponse(RecipeBase):
    recipe_id: UUID

    class Config:
        orm_mode = True
