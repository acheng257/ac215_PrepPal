from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_history import UserHistory
from schemas.user_history import UserHistoryResponse, UserHistoryCreate
from models.database import get_db
from typing import List

router = APIRouter()


@router.get("/user/{user_id}/history/recommendations", response_model=List[UserHistoryResponse])
async def get_user_history_recs(user_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(UserHistory).where(UserHistory.user_id == user_id, UserHistory.recommendation_data.isnot(None)).order_by(UserHistory.created_at.desc()).limit(5)
    result = await db.execute(stmt)
    history = result.scalars().all()

    return history


@router.post("/user/{user_id}/history", response_model=UserHistoryResponse, status_code=status.HTTP_201_CREATED)
async def update_user_history(user_id: UUID, history_data: UserHistoryCreate, db: AsyncSession = Depends(get_db)):
    """
    Update the user's history with new data in the database.
    """
    print(f"Received user id: {user_id}")
    new_history = UserHistory(user_id=user_id, details=history_data.details, recommendation_id=history_data.recommendation_id, recommendation_data=history_data.recommendation_data)

    db.add(new_history)

    try:
        await db.commit()
        await db.refresh(new_history)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    return new_history
