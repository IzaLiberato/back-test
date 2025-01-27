from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.database import engine, Base
import os
from dotenv import load_dotenv

load_dotenv()

API_PORT = os.getenv("API_PORT")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(API_PORT))
