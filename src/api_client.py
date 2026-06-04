import requests
class CountryLeadersAPI:
    def __init__(self):
        self.base_url: str = "https://country-leaders.onrender.com"
        self.country_endpoint: str = f"{self.base_url}/countries"
        self.leaders_endpoint: str = f"{self.base_url}/leaders"
        self.cookies_endpoint: str = f"{self.base_url}/cookie"
        self.session: requests.Session = requests.Session()

    def refresh_cookies(self):
        # Logic to refresh cookies
        response = self.session.get(self.cookies_endpoint)
        cookie_value = response.cookies.get('user_cookie')
        self.session.cookies.set('user_cookie', cookie_value)
        return self.session.cookies

    def get_countries(self) -> list:
        # Logic to get the list of countries
        countries = self.session.get(self.country_endpoint).json()
        return countries

    def get_leaders(self, country: str) -> list:
        # Logic to get the list of country leaders
        leaders_url = f"{self.leaders_endpoint}?country={country}"
        leaders = self.session.get(leaders_url).json()
        return leaders