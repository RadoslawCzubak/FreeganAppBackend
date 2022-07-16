from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    end_time = Column(Integer)
    company_id = Column(Integer, ForeignKey('companies.id'))

    products = relationship("Product", back_populates="offer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Integer)
    offer_id = Column(Integer, ForeignKey('offers.id'))

    offer = relationship("Offer", back_populates="products")
