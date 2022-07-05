from datetime import timedelta, datetime
from typing import Union

from passlib.context import CryptContext
from jose import JWTError, jwt

# temporary key
from freegan_app.db.db_repository import DbRepository

SECRET_KEY = "7bb30c52ce98dbd26fe3dd2550360eff3bdd6f15d052a005510445fd85aa3ce7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

fake_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db_repo: DbRepository, email):
    return db_repo.get_user_by_email(email)


def authenticate_user(db_repo, email: str, password: str):
    user = get_user(db_repo, email)
    if not user:
        return False
    if not verify_password(password, user.password_hashed):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_token_for_user(db_repo, username: str, password: str):
    user = authenticate_user(db_repo, username, password)
    if not user:
        return False
