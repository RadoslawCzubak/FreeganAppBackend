from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from freegan_app.domain.auth import create_token_for_user
from ..schemas.auth_schema import Token
from ..dependencies.dependencies import get_db_repository

router = APIRouter(tags=["Authorization"])


@router.post("/token")
async def login_user_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_repository)):
    token = create_token_for_user(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token, token_type="Bearer")
