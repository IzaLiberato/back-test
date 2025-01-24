from fastapi import FastAPI
from app.routers import users, auth
from app.database import engine, Base
import os
from dotenv import load_dotenv

load_dotenv()

API_PORT = os.getenv("API_PORT")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(API_PORT))
