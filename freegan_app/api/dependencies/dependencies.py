from freegan_app.db.database import SessionLocal
from freegan_app.db.db_repository import DbRepository


def get_db_repository():
    db = DbRepository(SessionLocal())
    try:
        yield db
    finally:
        db.close()
