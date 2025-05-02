from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import server.services.auth_service as auth
from server.dependencies import get_db
from shared.schemas.user_schema import UserCreate

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        await auth.create_user(db, user)
        return {"message": "User registered successfully"}
    except Exception as e:
        return {"message": str(e)}


@router.get("/me")
async def get_current_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await auth.get_current_user(db, telegram_id)
        if user:
            return user
        else:
            return {"message": "User not found"}
    except Exception as e:
        return {"message": str(e)}
