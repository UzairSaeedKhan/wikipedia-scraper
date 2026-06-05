import requests
from src import CountryLeadersAPI, WikipediaScraper, get_logger
logger = get_logger(__name__)
def main():
    '''
    Main function to connect the entire pipeline. It initializes the API client and scraper with a shared requests.Session, 
    then executes the steps to fetch countries, retrieve leaders, scrape Wikipedia bios, and save the results to a JSON file. 
    It also includes error handling to refresh cookies and retry if any step fails.
    '''
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
        while True:
            user_input = input("Do you want to save the results to json or csv?: ")
            if user_input == "json":
                scraper.to_json_file('leaders.json', leaders_by_countries)
                break
            elif user_input == "csv":
                scraper.to_csv_file('leaders.csv', leaders_by_countries)
                break
            else:
                print("Invalid input. Please enter 'json' or 'csv'.")

    except Exception as e:
        logger.info(f"Pipeline failed: {e}")
        api_client.refresh_cookies()  # refresh on failure and retry if needed

if __name__ == "__main__":
    main()