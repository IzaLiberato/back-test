from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.crud import create_user, get_users
from app.dependencies import get_admin_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return get_users(db)