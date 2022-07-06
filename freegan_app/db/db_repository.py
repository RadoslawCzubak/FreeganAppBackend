from freegan_app.db.database import SessionLocal
from freegan_app.db.model.user import User


class DbRepository:

    def __init__(self, db: SessionLocal):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_new_user(self, email: str, password_hashed: str):
        db_user = User(email=email, password_hashed=password_hashed)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def close(self):
        self.db.close()
