from typing import Union

from sqlalchemy.orm import Session

from freegan_app.db.model.company import Company


class DbCompanyRepository:

    def __init__(self, db: Session):
        self.db: Session = db

    def get_company_by_owner(self, user_id: int) -> Union[Company, None]:
        result = self.db.query(Company).where(Company.user_id == user_id).first()
        return result

    def create_new_company(self, name: str, address: str, lat: float, lon: float, user_id: int):
        db_company = Company(name=name, address=address, lat=lat, lon=lon, user_id=user_id)
        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company
