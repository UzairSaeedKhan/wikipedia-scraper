from src.html_scraper import WikipediaScraper
from src.api_client import CountryLeadersAPI
import requests
from src.logger import get_logger
logger = get_logger(__name__)
def main():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; my-script/1.0; your@email.com)"})
    
    api_client = CountryLeadersAPI(session)
    scraper = WikipediaScraper(session)

    try:
        logger.info("Pipeline started")
        api_client.refresh_cookies()  # refreshes cookies on the shared session
        countries = api_client.get_countries()
        leaders_by_countries = {}

        for country in countries:
            leaders = api_client.get_leaders(country)
            for leader in leaders:
                wiki_url = leader.get('wikipedia_url')
                if wiki_url:
                    html_content = scraper.fetch_html(wiki_url)
                    first_paragraph = scraper.get_first_paragraph(html_content)
                    leader['wikipedia_bio'] = scraper.clean_text(first_paragraph)
            leaders_by_countries[country] = leaders
        logger.info("Pipeline completed, saving to leaders.json")
        scraper.to_json_file('leaders.json', leaders_by_countries)

    except Exception as e:
        logger.info(f"Pipeline failed: {e}")
        api_client.refresh_cookies()  # refresh on failure and retry if needed

if __name__ == "__main__":
    main()