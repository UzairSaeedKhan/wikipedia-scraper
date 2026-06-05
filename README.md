# 🌍 Wikipedia Country Leaders Scraper

[![Made with Python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

![Wikipedia Scraper Banner](https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=900&auto=format&fit=crop&q=60)

## 📖 Description

A Python pipeline that pulls world leaders from a REST API, scrapes their Wikipedia biographies, cleans the text, and saves everything into a structured JSON file.

The scraper handles multiple languages (English, French, Dutch, Arabic, Russian) and automatically cleans up pronunciation markers, IPA symbols, references, and other Wikipedia noise so the output is clean and human-readable.

---

## 📦 Repo Structure

```
.
├── src/
│   ├── __init__.py
│   ├── api_client.py       # Handles all calls to the country-leaders API
│   ├── html_scraper.py     # Fetches and parses Wikipedia pages
│   └── logger.py           # Centralized logging setup
├── .gitignore
├── leaders.json            # Output file generated after running the script
├── main.py                 # Entry point — coordinates the full pipeline
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/UzairSaeedKhan/wikipedia-scraper.git
   cd wikipedia-scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv wikipedia_scraper_env
   source wikipedia_scraper_env/bin/activate  # on Windows: wikipedia_scraper_env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛎️ Usage

Run the pipeline with:

```bash
python3 main.py
```

The script will:
- Refresh the API session cookie automatically
- Fetch the list of available countries
- Retrieve all leaders per country
- Scrape and clean each leader's Wikipedia first paragraph
- Save the full dataset to `leaders.json`

---

## 🖼️ Visuals

**Pipeline flow:**

![Pipeline](https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=800&auto=format&fit=crop&q=60)

**Sample output in `leaders.json`:**

```json
{
    "us": [
        {
            "first_name": "Barack",
            "last_name": "Obama",
            "wikipedia_bio": "Barack Hussein Obama II (born August 4, 1961) is an American politician who served as the 44th president of the United States from 2009 to 2017."
        }
    ]
}
```

**Runtime logs:**

```
2026-06-05 10:23:01 - src.api_client - INFO - Refreshing cookies...
2026-06-05 10:23:02 - src.api_client - INFO - Fetching leaders for us...
2026-06-05 10:23:03 - src.html_scraper - INFO - Fetching HTML for https://en.wikipedia.org/wiki/Barack_Obama
2026-06-05 10:23:18 - main - INFO - Pipeline completed, saving to leaders.json
```

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| `requests` | HTTP requests and session management |
| `BeautifulSoup` | HTML parsing |
| `re` | Text cleaning with regex |
| `json` | Saving output data |
| `logging` | Runtime tracking and warnings |

---

## ⏱️ Timeline

Completed in **3 days** as part of the AI Bootcamp at [BeCode.org](https://becode.org/).

---

## 👤 Contributors

**Uzair Saeed Khan**  
Connect on [LinkedIn](https://www.linkedin.com/in/uzairsaeedkhan/) · [GitHub](https://github.com/UzairSaeedKhan)
