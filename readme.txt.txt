BookSpider - A Scrapy Web Scraper
=================================

Description
-----------
BookSpider is a web scraping project built with Scrapy. 
It scrapes book data such as title, price, availability, rating, and number of reviews from an online bookstore. 
The scraped data can be stored in JSON, CSV, or directly into a MySQL database.

Project Structure
-----------------
bookscraper/
│
├── bookscraper/        # Main Scrapy project directory
│   ├── spiders/        # Contains the spider code (bookspider.py)
│   ├── items.py        # Defines the data fields to be scraped
│   ├── pipelines.py    # Handles data cleaning and saving (MySQL, JSON, etc.)
│   └── settings.py     # Scrapy project settings
│
└── scrapy.cfg          # Scrapy configuration file

Requirements
------------
- Python 3.9+
- Scrapy
- MySQL Server (optional, if storing in DB)
- MySQL Connector (for Python)

Installation
------------
1. Clone or download the project.
2. Create a virtual environment and activate it.
3. Install dependencies:
   pip install scrapy mysql-connector-python

Usage
-----
To run the spider and save data to JSON:
   scrapy crawl bookspider -O booksdata.json

To run the spider and save data to CSV:
   scrapy crawl bookspider -O booksdata.csv

If using MySQL, configure your database connection inside `pipelines.py`.

Output
------
Depending on configuration, the scraper will output:
- booksdata.json
- booksdata.csv
- Books table in MySQL database

License
-------
This project is for educational purposes only. Use responsibly.
