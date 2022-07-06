from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from freegan_app.api.dependencies.dependencies import check_token_and_return_user
from freegan_app.api.routers import auth_router
from freegan_app.db.database import create_db_tables

create_db_tables()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/auth/test")
async def auth_test(user=Depends(check_token_and_return_user)):
    return {"user": user}


app.include_router(auth_router.router)
