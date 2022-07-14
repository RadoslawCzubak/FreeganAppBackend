from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from freegan_app.api.schemas.user_schema import User
from freegan_app.db.database import SessionLocal
from freegan_app.db.repository.db_auth_repository import DbAuthRepository
from freegan_app.db.repository.db_company_repository import DbCompanyRepository
from freegan_app.domain import auth, company
from freegan_app.domain.auth import AuthError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_auth_repository(session=Depends(get_db_session)):
    return DbAuthRepository(session)


def get_db_company_repository(session=Depends(get_db_session)):
    return DbCompanyRepository(session)


def check_token_and_return_user(token: str = Depends(oauth2_scheme), db_repo=Depends(get_db_auth_repository)):
    result = auth.get_current_user(token, db_repo)
    if result == AuthError.UNAUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


def check_user_and_return_company(user: User = Depends(check_token_and_return_user),
                                  db_repo: DbCompanyRepository = Depends(get_db_company_repository)):
    print(user)
    cmp = company.get_company(db_repo, user.id)
    if not cmp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return cmp
