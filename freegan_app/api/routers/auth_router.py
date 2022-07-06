from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import freegan_app.domain.auth as auth
from ..schemas.auth_schema import Token
from ..schemas.user_schema import RegisterUserPostRequest, User
from ..dependencies.dependencies import get_db_repository

router = APIRouter(prefix="/user", tags=["Authorization"])


@router.post("/token", response_model=Token)
async def login_user_for_token(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_repository)):
    token = auth.create_token_for_user(db, user.username, user.password)
    if token == auth.AuthError.WRONG_CREDENTIALS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token, token_type="Bearer")


@router.post("/register", response_model=User)
async def register_user(user: RegisterUserPostRequest, db=Depends(get_db_repository)):
    result = auth.create_new_user(db, email=user.email, password=user.password)
    if result == auth.AuthError.USER_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif result == auth.AuthError.PASSWORD_TOO_WEAK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too weak.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result
