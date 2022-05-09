Data Engineering Project

Scrapes News Websites to gather keywords for analysis

Setting up:
create virtual environment in /venv

Activate virtual environment:
source venv/bin/activate

Install packages:
pip install -r requirements.txt

Run the tests:
python -m pytest -q scripts/tests/test_parser.py

Run the scraper:
python scripts/scraper.py

Run the parser:
python scripts/parser.py

Run the sentiment classifier:
python scripts/sentiment.py
