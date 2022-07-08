from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    address: str
    lat: float
    lon: float


class CreateCompanyPostRequest(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
