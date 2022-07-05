from freegan_app.db.database import SessionLocal
from freegan_app.db.model.user import User


class DbRepository:

    def __init__(self, db: SessionLocal):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def close(self):
        self.db.close()
