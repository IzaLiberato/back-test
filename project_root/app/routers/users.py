from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.crud import create_user, get_users
from app.dependencies import get_admin_user
from app.models import User


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201, summary="Cadastrar um novo usuário")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    return create_user(db, user)

@router.get("/", response_model=List[UserResponse], summary="Listar todos os usuários", description="Apenas administradores podem acessar este endpoint.", )
def list_users(db: Session = Depends(get_db), admin_user=Depends(get_admin_user)):
    return get_users(db)

@router.put("/promote/{user_id}", summary="Promover usuário a administrador", description="Este endpoint só pode ser acessado por administradores.")
def promote_user(user_id: int, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    if user.is_admin:
        raise HTTPException(status_code=400, detail="O usuário já é um administrador.")

    user.is_admin = True
    db.commit()
    db.refresh(user)

    return {"msg": f"Usuário {user.email} promovido a administrador."}
