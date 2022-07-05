from fastapi import FastAPI
from freegan_app.api.routers import auth_router
from freegan_app.db.database import create_db_tables

create_db_tables()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


app.include_router(auth_router.router)
