from sqlalchemy import Column, Boolean, Integer, String
from ..database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hashed = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String)

