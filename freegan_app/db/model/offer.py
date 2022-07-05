from sqlalchemy import Column, ForeignKey, Integer, String
from ..database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    end_time = Column(String)
    company_id = Column(Integer, ForeignKey('company.id'))
