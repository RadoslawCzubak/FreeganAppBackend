from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from freegan_app.db.database import SessionLocal
from freegan_app.db.repository.db_auth_repository import DbAuthRepository
from freegan_app.domain import auth
from freegan_app.domain.auth import AuthError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_db_repository():
    db = DbAuthRepository(SessionLocal())
    try:
        yield db
    finally:
        db.close()


def check_token_and_return_user(token: str = Depends(oauth2_scheme), db_repo=Depends(get_db_repository)):
    result = auth.get_current_user(token, db_repo)
    if result == AuthError.UNAUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result
