from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class RegisterUserPostRequest(UserBase):
    password: str


class LoginUserPostRequest(UserBase):
    password: str


class User(UserBase):
    id: int
    password_hashed: str

    class Config:
        orm_mode = True
