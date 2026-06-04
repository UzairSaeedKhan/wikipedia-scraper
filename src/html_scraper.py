
from bs4 import BeautifulSoup, soup
import json, requests, re

class WikipediaScraper:
    def __init__(self, session):
        self.session = session
    
    def fetch_html(self, url: str) -> str:
        # Fetches the HTML content of the given URL using the requests library, ensuring that the session is properly managed 
        # and that any potential issues with the request are handled gracefully.
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Check if the request was successful
            return response.text
        except requests.RequestException as req_err:
            print(f"Request error occurred while fetching {url}: {req_err}")
            raise
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while fetching {url}: {http_err}")
            raise
        except requests.ConnectionError as e:
            print(f"Connection error occurred while fetching {url}: {e}")
            raise

    def get_first_paragraph(self, html: str) -> str:
        # Parses the HTML content to extract the first meaningful paragraph, ensuring that it is not empty or just a reference.
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
        # Cleans the extracted text by removing unwanted characters, references, and formatting using regular expressions.
        regex_patterns = [r'\[.*?\]|\(\/.*?\/\)|<.*?>|\n|\xa0', r'\[\[(?:[^\]]*?\|)?([^\]]+)\]\]', r'Écouterⓘ', r'Prononciationⓘ', r'(\s)+', r'(\s)+', r'(\s)+']
        for pattern in regex_patterns:
            text = re.sub(pattern, '', text).strip()
        return text
    
    def to_json_file(self, filepath: str, data: str) -> None:
        # stores the data structure into a JSON file, ensuring that the file is properly formatted and human-readable.
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)