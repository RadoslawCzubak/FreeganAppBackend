from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class RegisterUserPostRequest(UserBase):
    password: str


class LoginUserPostRequest(UserBase):
    password: str


class RegisterUserPostResponse(UserBase):
    id: int
    is_verified: bool = False


class User(UserBase):
    id: int
    password_hashed: str
    is_verified: bool = False
    verification_code: str

    class Config:
        orm_mode = True
