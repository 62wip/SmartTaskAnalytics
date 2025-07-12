from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserCreate, UserResponse
from src.crud.user import create_user, get_user_by_email, get_user_by_username
from src.db.session import get_session

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    existing_user = await get_user_by_email(session, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_user = await get_user_by_username(session, user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already used")

    user = await create_user(session, user_in.username, user_in.email, user_in.password)
    return user