from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from models.database import get_db
from models.pantry import PantryItem
from schemas.pantry import PantryUpdate, PantryResponse, PantryCreate
from ..utils.llm_rag_utils import update_pantry_with_llm

router = APIRouter()


@router.get("/{user_id}", response_model=PantryResponse)
async def get_user_pantry(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(PantryItem).where(PantryItem.user_id == user_id))
        pantry_item = result.scalars().first()

        if pantry_item is None:
            new_pantry_item = PantryItem(user_id=user_id, items={})
            db.add(new_pantry_item)
            await db.commit()
            await db.refresh(new_pantry_item)
            pantry_item = new_pantry_item

        # Ensure items is a dictionary, use an empty dict if it's None
        items = pantry_item.items if pantry_item.items is not None else {}

        return PantryResponse(user_id=pantry_item.user_id, items=items, last_updated=pantry_item.last_updated)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{user_id}", response_model=PantryResponse)
async def update_user_pantry(user_id: UUID, pantry_update: PantryUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(PantryItem).where(PantryItem.user_id == user_id))
        pantry_item = result.scalars().first()

        if pantry_item is None:
            pantry_create = PantryCreate(items=pantry_update.items or {})
            new_pantry_item = PantryItem(user_id=user_id, **pantry_create.dict())
            db.add(new_pantry_item)
            await db.commit()
            await db.refresh(new_pantry_item)
            pantry_item = new_pantry_item
        else:
            if pantry_update.items is not None:
                updated_pantry = update_pantry_with_llm(pantry=pantry_update.items, used_ingredients=pantry_update.ingredients)
                pantry_item.items = updated_pantry
            db.add(pantry_item)
            await db.commit()
            await db.refresh(pantry_item)

        return PantryResponse(user_id=pantry_item.user_id, items=pantry_item.items, last_updated=pantry_item.last_updated)

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_pantry(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(PantryItem).where(PantryItem.user_id == user_id))
        pantry_item = result.scalars().first()

        if pantry_item is None:
            raise HTTPException(status_code=404, detail="User pantry not found")

        await db.delete(pantry_item)
        await db.commit()

        return {"message": "Pantry deleted successfully", "user_id": str(user_id)}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
