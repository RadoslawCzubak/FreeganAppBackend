from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import freegan_app.domain.auth as auth
from ..schemas.auth_schema import Token
from ..schemas.user_schema import LoginUserPostRequest, RegisterUserPostRequest
from ..dependencies.dependencies import get_db_repository

router = APIRouter(prefix="/user", tags=["Authorization"])


@router.post("/token", response_model=Token)
async def login_user_for_token(user: LoginUserPostRequest, db=Depends(get_db_repository)):
    token = auth.create_token_for_user(db, user.email, user.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token, token_type="Bearer")


@router.post("/register")
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
