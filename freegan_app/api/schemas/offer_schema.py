from typing import List

from pydantic import BaseModel

from freegan_app.api.schemas.product_schema import Product, CreateProductRequest


class OfferBase(BaseModel):
    end_time: int


class CreateOfferRequest(OfferBase):
    products: List[CreateProductRequest]


class Offer(OfferBase):
    id: int
    products: List[Product]

    class Config:
        orm_mode = True
