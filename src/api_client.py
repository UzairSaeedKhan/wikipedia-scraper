import requests
from src.logger import get_logger
logger = get_logger(__name__)

class CountryLeadersAPI:
    def __init__(self, session: requests.Session):
        self.base_url: str = "https://country-leaders.onrender.com"
        self.country_endpoint: str = f"{self.base_url}/countries"
        self.leaders_endpoint: str = f"{self.base_url}/leaders"
        self.cookies_endpoint: str = f"{self.base_url}/cookie"
        self.session = session  # use the shared session instead of creating a new one

    def refresh_cookies(self):
        logger.info("Refreshing cookies...")
        response = self.session.get(self.cookies_endpoint)
        cookie_value = response.cookies.get('user_cookie')
        self.session.cookies.set('user_cookie', cookie_value, domain='country-leaders.onrender.com')
        logger.info("Cookies refreshed successfully")

    def get_countries(self):
        logger.info("Fetching countries...")
        return self.session.get(self.country_endpoint).json()

    def get_leaders(self, country):
        logger.info(f"Fetching leaders for {country}...")
        return self.session.get(f"{self.leaders_endpoint}?country={country}").json()