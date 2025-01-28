# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import uuid
from passlib.context import CryptContext

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    from app.models import User

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == 'admin@fastapi.com').first()
        if not admin:
            hashed_password = pwd_context.hash("senha123")
            admin_user = User(
                id=str(uuid.uuid4()),
                email='admin@fastapi.com',
                password=hashed_password,
                is_admin=True,
                name="Admin",
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("Usuário administrador criado automaticamente!")
        else:
            print("Usuário administrador já existe.")
    except Exception as e:
        print(f"Erro ao rodar seed: {e}")
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    seed_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
