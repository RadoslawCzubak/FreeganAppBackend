from sqlalchemy import Column, ForeignKey, Integer, String
from ..database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Integer)
    offer_id = Column(Integer)
