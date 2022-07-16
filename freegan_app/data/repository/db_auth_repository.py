from sqlalchemy.orm import Session

from freegan_app.data.database import SessionLocal
from freegan_app.data.model.user_model import User


class DbAuthRepository:
    def __init__(self, db: SessionLocal):
        self.db: Session = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_new_user(self, email: str, password_hashed: str, verification_code: str):
        db_user = User(email=email, password_hashed=password_hashed, verification_code=verification_code)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def set_user_verification_status(self, user_id, is_verified):
        self.db.query(User).filter(User.id == user_id).update({"is_verified": is_verified})
        self.db.commit()
        return

    def close(self):
        self.db.close()
