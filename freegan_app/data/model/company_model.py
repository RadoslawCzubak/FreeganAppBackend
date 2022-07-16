from sqlalchemy import Column, Integer, String, Float, ForeignKey
from ..database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    address = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    user_id = Column(Integer, ForeignKey('user.id'))
