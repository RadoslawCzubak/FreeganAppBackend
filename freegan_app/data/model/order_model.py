from sqlalchemy import Column, ForeignKey, Integer, String
from ..database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    amount_ordered = Column(Integer)
    user_id = Column(Integer)
    product_id = Column(Integer)
