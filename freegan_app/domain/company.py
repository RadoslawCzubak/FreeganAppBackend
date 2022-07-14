from freegan_app.api.schemas.offer_schema import CreateOfferRequest
from freegan_app.db.repository.db_company_repository import DbCompanyRepository


class CompanyError:
    COMPANY_EXISTS = 1
    INVALID_NAME = 2
    INVALID_COORDS = 3
    NOT_EXISTS = 4
    CREATE_OFFER_ERROR = 5


def get_company(db_repo: DbCompanyRepository, user_id: int):
    company = db_repo.get_company_by_owner(user_id)
    if not company:
        return CompanyError.NOT_EXISTS
    return company


def create_new_company(db_repo: DbCompanyRepository, name: str, address: str, lat: float, lon: float, user_id: int):
    company = db_repo.get_company_by_owner(user_id)
    if company:
        return CompanyError.COMPANY_EXISTS
    if len(name) == 0:
        return CompanyError.INVALID_NAME
    if not is_lat_valid(lat) or not is_lon_valid(lon):
        return CompanyError.INVALID_COORDS
    return db_repo.create_new_company(name, address, lat, lon, user_id)


def is_lat_valid(lat: float) -> bool:
    if -90.0 <= lat <= 90.0:
        return True
    return False


def is_lon_valid(lon: float) -> bool:
    if -180.0 <= lon <= 180.0:
        return True
    return False


def create_offer(db_repo: DbCompanyRepository, offer: CreateOfferRequest, user_id: int):
    company = get_company(db_repo, user_id)
    if not company:
        return CompanyError.NOT_EXISTS
    result = db_repo.create_offer(offer, company_id=company.id)
    if not result:
        return CompanyError
    return result


def get_all_offers(db_repo: DbCompanyRepository):
    offers = db_repo.get_all_offers()
    if not offers:
        return []
    return offers


def get_company_offers(db_repo: DbCompanyRepository, company_id: int):
    offers = db_repo.get_offers_by_company(company_id)
    if not offers:
        return []
    return offers


def get_offer_by_id(db_repo: DbCompanyRepository, offer_id: int):
    offer = db_repo.get_offer_by_id(offer_id)
    if not offer:
        return CompanyError.NOT_EXISTS
    return offer


def get_latest_company_offer(db_repo: DbCompanyRepository, company_id: int):
    offer = db_repo.get_latest_company_offer(company_id)
    offer.products
    if not offer:
        return CompanyError.NOT_EXISTS
    return offer
