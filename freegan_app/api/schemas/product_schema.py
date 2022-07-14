from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    amount: int


class CreateProductRequest(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
