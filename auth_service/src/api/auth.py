from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserResponse
from src.crud.user import create_user, get_user_by_email, get_user_by_username
from src.db.session import get_session

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_session)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    user = create_user(db, user_in.username, user_in.email, user_in.password)
    return user
