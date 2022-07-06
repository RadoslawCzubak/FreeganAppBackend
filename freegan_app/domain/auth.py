from datetime import timedelta, datetime
from typing import Union

from fastapi import Depends
from passlib.context import CryptContext
from jose import JWTError, jwt

# temporary key
from freegan_app.api.dependencies.dependencies import get_db_repository
from freegan_app.api.schemas.user_schema import User
from freegan_app.db.db_repository import DbRepository

SECRET_KEY = "7bb30c52ce98dbd26fe3dd2550360eff3bdd6f15d052a005510445fd85aa3ce7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthError:
    WRONG_CREDENTIALS = 1
    USER_EXISTS = 2
    PASSWORD_TOO_WEAK = 3
    USER_INACTIVE = 4
    UNAUTHORIZED = 5


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db_repo: DbRepository, email):
    return db_repo.get_user_by_email(email)


def authenticate_user(db_repo, email: str, password: str) -> Union[User, bool]:
    user = get_user(db_repo, email)
    if not user:
        return False
    if not verify_password(password, user.password_hashed):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_token_for_user(db_repo: DbRepository, email: str, password: str) -> Union[int, str]:
    user = authenticate_user(db_repo, email, password)
    if not user:
        return AuthError.WRONG_CREDENTIALS
    return create_access_token(
        {
            "sub": user.id,
            "email": user.email
        }
    )


def create_new_user(db_repo: DbRepository, email: str, password: str) -> Union[User, int]:
    user = get_user(db_repo, email)
    if user:
        return AuthError.USER_EXISTS
    if not check_password_strength(password):
        return AuthError.PASSWORD_TOO_WEAK
    password_hashed = get_password_hash(password)
    return db_repo.create_new_user(email, password_hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


def check_password_strength(password: str):
    return len(password) >= 8


def get_current_user(token: str, db_repo: DbRepository = Depends(get_db_repository)) -> Union[User, int]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return AuthError.UNAUTHORIZED
    except JWTError:
        return AuthError.UNAUTHORIZED
    user = db_repo.get_user_by_id(user_id)
    if user is None:
        return AuthError.UNAUTHORIZED
    return user