# KlikIndomaret Web Scraper

This Python project automates the process of scraping product data from KlikIndomaret's website. It utilizes `Selenium` for automating browser interactions and `BeautifulSoup` for parsing HTML content. The scraper allows you to extract product details from categories, including product name, price, and more.

## Features

- **Scrapes Products from Categories**: Extracts product information like title, price, discounts, PLU, and more from multiple pages in a product category.
- **Supports Multiple Sorting Options**: Sort by promo, popularity, price, and more.
- **Handles Multiple Pages**: Automatically navigates through paginated category results.
- **JSON Output**: The scraper can return product data as a JSON string or a Python list.
- **Category Extraction**: Decodes product categories and subcategories from the HTML structure.
- **Price Parsing**: Converts Rupiah price strings to integers for ease of processing.

## Requirements

- Python 3.x
- Selenium WebDriver for browser automation (e.g., Firefox)
- `beautifulsoup4` for HTML parsing
- `lxml` (Optional) for fast and efficient XML/HTML processing

Install the required packages via pip:

```bash
pip install selenium beautifulsoup4
```

## Usage
### Initializing the Scraper

To start scraping, initialize the `SeleniumKlikIndomaretScrapper` class with a `selenium.webdriver` instance:

```python
from selenium import webdriver
from scrapper import SeleniumKlikIndomaretScrapper

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox()  # or any other webdriver
scraper = SeleniumKlikIndomaretScrapper(driver, bs4_parser='html.parser') # or any other beatifulsoup parser e.g., lxml
```

### Extracting Products from a Category Page

You can scrape products from a category page by calling the `get_products_from_category` method:

```python
category_link = "/category/sarapan"
products_page_1 = scraper.get_products_from_category(category_link, page=1)
print(products_page_1)
```

Or you can let the class handles multiple pages automatically (but this is discouraged, because the scraper can be 
easily detected by cloudflare and therefore be blocked) by calling the `get_all_products_from_category` method:

```python
category_link = "/category/sarapan"
products = scraper.get_all_products_from_category(category_link)
print(products)
```

Both method will return a list of products or JSON with structure like this:

```json
[
  {
    "plu": "20133182",
    "link": "https://www.klikindomaret.com/product/100-natural-honey",
    "title": "Uray 100% Natural Honey 150G",
    "category": "Sarapan",
    "price": 9900,
    "old_price": 24900,
    "discount": "60%",
    "is_discount": true,
    "is_flash_sale": false
  },
]
```

### Saving Data to JSON

To save the scraped data to a JSON file, use the `save_json_to_file` function:

```python
from util import save_json_to_file

json_data = scraper.get_all_products_from_category(category_link, return_in_json=False)
save_json_to_file(json_data, "hasil", "products.json")
```

Check [`main.py`](selenium_main.py) for more detail.

## TODO

- [ ] Rewrite scraper using Scrapy
- [ ] Write test

