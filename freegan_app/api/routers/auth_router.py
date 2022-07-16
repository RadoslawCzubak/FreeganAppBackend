from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import freegan_app.core.auth as auth
from ..schemas.auth_schema import Token
from ..schemas.user_schema import RegisterUserPostRequest, RegisterUserPostResponse, VerifyUserRequest
from ..dependencies.dependencies import get_db_auth_repository
from freegan_app.api.email_verification.email_sender import send_verification_email

router = APIRouter(prefix="/user", tags=["Authorization"])


@router.post("/token", response_model=Token)
async def login_user_for_token(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_auth_repository)):
    token = auth.create_token_for_user(db, user.username, user.password)
    if token == auth.AuthError.WRONG_CREDENTIALS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if token == auth.AuthError.USER_INACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token, token_type="Bearer")


@router.post("/verify")
async def verify_user(user_info: VerifyUserRequest, db=Depends(get_db_auth_repository)):
    result = auth.verify_user(db, user_info.email, user_info.verification_code)
    if result == auth.AuthError.WRONG_CREDENTIALS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect verification code",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return


@router.post("/register", response_model=RegisterUserPostResponse)
async def register_user(user: RegisterUserPostRequest, db=Depends(get_db_auth_repository)):
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
    send_verification_email(result.email, result.verification_code)
    return RegisterUserPostResponse(id=result.id, email=result.email, is_verified=result.is_verified)
