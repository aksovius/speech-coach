from fastapi.responses import JSONResponse
import services.auth as auth
from schemas.user import User
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db

@router.post("/register")
async def register_user(user: User, db: AsyncSession = Depends(get_db)):
    try:
        await auth.get_or_create_user_by_telegram_id(db, user)
        return JSONResponse(status_code=201, content={"message": "User registered successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})