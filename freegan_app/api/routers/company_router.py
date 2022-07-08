from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import freegan_app.domain.company as company
from freegan_app.api.dependencies import dependencies
from freegan_app.api.dependencies.dependencies import check_token_and_return_user
from freegan_app.api.schemas.company_schema import CreateCompanyPostRequest, Company

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("/", response_model=Company)
async def get_my_company(user=Depends(check_token_and_return_user),
                         db=Depends(dependencies.get_db_company_repository)):
    result = company.get_company(db, user.id)
    if result == company.CompanyError.NOT_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company doesn't exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


@router.post("/")
async def create_new_company(new_company: CreateCompanyPostRequest, user=Depends(check_token_and_return_user),
                             db=Depends(dependencies.get_db_company_repository)):
    result = company.create_new_company(db, new_company.name, new_company.address, new_company.lat, new_company.lon,
                                        user.id)
    if result == company.CompanyError.COMPANY_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if result == company.CompanyError.INVALID_NAME:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect company name.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if result == company.CompanyError.INVALID_COORDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect coordinates.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result
