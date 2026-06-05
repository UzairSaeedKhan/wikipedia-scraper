from bs4 import BeautifulSoup
import json, requests, re, csv
from src.logger import get_logger
logger = get_logger(__name__)

class WikipediaScraper:
    '''
    A class responsible for fetching and processing HTML content from Wikipedia pages, 
    extracting relevant information, and saving it in a structured format.
    '''
    def __init__(self, session):
        self.session = session
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; my-script/1.0; your@email.com)"
    })
    
    def fetch_html(self, url: str) -> str:
        '''
        Fetches the HTML content of the given URL using the requests library, ensuring that the session is properly managed 
        and that any potential issues with the request are handled gracefully.
        '''
        logger.info(f"Fetching HTML for {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Check if the request was successful
            return response.text
        except requests.RequestException as req_err:
            logger.warning(f"Request failed for {url}: {req_err}")
            raise
        except requests.HTTPError as http_err:
            logger.warning(f"Request failed for {url}: {http_err}")
            raise
        except requests.ConnectionError as e:
            logger.warning(f"Connection error occurred while fetching {url}: {e}")
            raise

    def get_first_paragraph(self, html: str) -> str:
        '''
        Parses the HTML content to extract the first meaningful paragraph, ensuring that it is not empty or just a reference.
        '''
        logger.debug("Extracting first paragraph...")
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = []
        for paragraph in soup.find_all('p'):
            paragraphs.append(paragraph.text)
        for paragraph in paragraphs:
            if len(paragraph.strip()) > 100:
                first_paragraph = paragraph
                break
        return first_paragraph
    
    def clean_text(self, text: str) -> str:
        '''
        Cleans the extracted text by removing references, HTML tags, and other unwanted characters, 
        ensuring that the resulting text is clean and human readable.
        '''
        patterns = [
            r'\[.*?\]',              # removes references like [1], [a]
            r'<.*?>',                # removes remaining HTML tags
            r'\n|\xa0',              # removes newlines and non-breaking spaces
            r'\([^)]*ⓘ[^)]*\)',      # removes pronunciation wikipedia tags
            r'\(\/[^)]+\/\)',        # removes IPA blocks unreadable help wikipedia tags
            r'\([^)]*МФА:[^)]*\)',   # removes Russian Cyrillic pronunciation blocks
            r'ⓘ',                    # removes ⓘ
            r'uitspraak|Écouter|Prononciation',  # removes audio/pronunciation labels
            r'\s+',                  # multiple spaces converted into one
        ]
        for pattern in patterns:
            replacement = ' ' if pattern == r'\s+' else ''
            text = re.sub(pattern, replacement, text)
        return text.strip()

    def to_json_file(self, filepath: str, data: dict) -> None:
        '''
        Stores the data structure into a JSON file, ensuring that the file is properly formatted and human-readable.
        '''
        logger.debug(f"Writing data to JSON file: {filepath}")
        # here it is important to add ensure_ascii flag and encoding for handling different languages and special characters in the text
        with open(filepath, 'w', encoding='utf-8') as f:
             json.dump(data, f, ensure_ascii=False, indent=4)

    def to_csv_file(self, filepath: str, data: dict) -> None:
        '''
        Stores the data structure into a CSV file, ensuring that the file is properly formatted and can be easily opened in spreadsheet software.
        '''
        logger.debug(f"Writing data to CSV file: {filepath}")
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Country', "id", "first_name", "last_name", "birth_date", "death_date", "place_of_birth", "wikipedia_url", "start_mandate", "end_mandate", "wikipedia_bio"])
            for country, leaders in data.items():
                for leader in leaders:
                    writer.writerow([
                        country,
                        leader.get("id", ""),
                        leader.get("first_name", ""),
                        leader.get("last_name", ""),
                        leader.get("birth_date", ""),
                        leader.get("death_date", ""),
                        leader.get("place_of_birth", ""),
                        leader.get("wikipedia_url", ""),
                        leader.get("start_mandate", ""),
                        leader.get("end_mandate", ""),
                        leader.get("wikipedia_bio", "")
                    ])