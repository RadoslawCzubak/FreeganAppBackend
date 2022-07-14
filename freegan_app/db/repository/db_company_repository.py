from typing import Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from freegan_app.api.schemas.offer_schema import CreateOfferRequest
from freegan_app.db.model.company import Company
from freegan_app.db.model.offer import Offer, Product


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

    def create_offer(self, offer: CreateOfferRequest, company_id: int):
        created_offer = Offer(end_time=offer.end_time, company_id=company_id)
        self.db.add(created_offer)
        self.db.commit()
        self.db.refresh(created_offer)
        for prod in offer.products:
            self.db.add(Product(name=prod.name, amount=prod.amount, offer_id=created_offer.id))
        self.db.commit()
        self.db.refresh(created_offer)
        return created_offer

    def get_all_offers(self):
        return self.db.query(Offer).all()

    def get_offers_by_company(self, company_id: int):
        return self.db.query(Offer).filter(Offer.company_id == company_id).all()

    def get_offer_by_id(self, offer_id: int):
        return self.db.query(Offer).filter(Offer.id == offer_id).first()

    def get_latest_company_offer(self, company_id: int):
        return self.db.query(Offer).filter(Offer.company_id == company_id).order_by(desc(Offer.id)).first()
