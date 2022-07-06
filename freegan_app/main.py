from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from freegan_app.api.routers import auth_router
from freegan_app.db.database import create_db_tables
from freegan_app.domain.auth import get_current_user

create_db_tables()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/items/")
async def read_items(token: str = Depends(get_current_user)):
    return {"token": token}

app.include_router(auth_router.router)
