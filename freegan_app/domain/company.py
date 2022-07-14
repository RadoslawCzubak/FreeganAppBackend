from freegan_app.db.repository.db_company_repository import DbCompanyRepository


class CompanyError:
    COMPANY_EXISTS = 1
    INVALID_NAME = 2
    INVALID_COORDS = 3
    NOT_EXISTS = 4


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
