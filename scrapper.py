from typing import Any

from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from json import JSONEncoder

import logging

from decoder import decode_categories, decode_products


class SeleniumKlikIndomaretScrapper:

    def __init__(self, driver: webdriver, bs4_parser: str = 'html.parser'):
        self.driver = driver
        self.json_encoder = JSONEncoder()
        self.base_url = 'https://www.klikindomaret.com'
        self.base_url_no_https = 'www.klikindomaret.com'
        self.bs4_parser = bs4_parser

    def get_all_products_from_category(
            self,
            category_link: str,
            sort_by: str = "PROMO",
            product_brand_id: str = None,
            start_price: int = None,
            end_price: int = None,
            attributes: str = None,
            show_item: str = None,
            return_in_json: bool = True,
            print_log: bool = False
    ) -> str | list[dict[str, Any]]:
        """
        Retrieves all products from a specified category, paginated across multiple pages,
        and returns the result in JSON format or as a list of dictionaries. Navigates through paginated category
        pages using Selenium WebDriver.

        Example of returned JSON structure::

        [
            {
                "plu": "20010381",
                "link": "https://www.klikindomaret.com/product/shampoo-ad-23512",
                "title": "Lifebuoy Shampoo Anti Dandruff 170Ml",
                "price":  15900,
                "category": "Perawatan Rambut",
                "old_price": 26900,
                "discount": "41%",
            },
        ]

        :param category_link: Whole or part of the category page URL
        :param product_brand_id: An optional product brand ID to filter products by brand.
        :param sort_by: Sorting criteria. The possible value is: PROMO, populer, terbaru, alfabet(a-z), alfabet(z-a), harga terendah, harga tertinggi.
        :param start_price: Start price in rupiah
        :param end_price: End price in rupiah
        :param attributes: Attributes
        :param show_item: Specify the provider to use. 'TI' for Toko Indomaret or '26' for Warehouse Jakarta 1
        :param return_in_json: Return in JSON string or in list object
        :param print_log: Print link, number of page, and product result in python logging
        :return: JSON or object about the products in this category
        """
        first_page_url = self._category_query_builder(
            category_link, 1, 54, sort_by, product_brand_id, start_price, end_price, attributes, show_item
        )

        first_page_content = self.load_page(first_page_url, 'wrp-produk-list')
        first_page_soup = BeautifulSoup(first_page_content, self.bs4_parser)
        num_page = len(
            first_page_soup \
                .find("select", class_="form-control pagelist") \
                .find_all("option", recursive=False)
        )

        if print_log:
            logging.info(f"Number Of Page: {num_page}")
            logging.info(first_page_url)

        products_result = decode_products(first_page_soup)
        if print_log:
            logging.debug(products_result)

        for i in range(1, num_page):
            self.driver.implicitly_wait(5)
            ActionChains(self.driver) \
                .send_keys(Keys.SPACE) \
                .perform()

            next_button = self.driver.find_element(by=By.CLASS_NAME, value="next")
            next_button.click()
            self.driver.implicitly_wait(5)
            ActionChains(self.driver) \
                .send_keys(Keys.SPACE) \
                .perform()

            self.wait_for_page('wrp-produk-list', 10)

            page_content = self.driver.page_source
            page_soup = BeautifulSoup(page_content, self.bs4_parser)

            page_result = decode_products(page_soup)

            if print_log:
                logging.debug(page_result)

            products_result.extend(page_result)

        if return_in_json:
            return self.json_encoder.encode(products_result)
        else:
            return products_result

    def get_products_from_category(
            self,
            category_link: str,
            page: int = 1,
            page_size: int = 54,
            sort_by: str = "PROMO",
            product_brand_id: str = None,
            start_price: int = None,
            end_price: int = None,
            attributes: str = None,
            show_item: str = None,
            return_in_json: bool = True,
            print_log: bool = False
    ) -> str | list[dict[str, Any]]:
        """
        Get products from a single page of category in KlikIndomaret

        Example of returned JSON structure::

        [
            {
                "plu": "20010381",
                "link": "https://www.klikindomaret.com/product/shampoo-ad-23512",
                "title": "Lifebuoy Shampoo Anti Dandruff 170Ml",
                "price":  15900,
                "category": "Perawatan Rambut",
                "old_price": 26900,
                "discount": "41%",
            },
        ]

        :param category_link: Whole or part of the category page URL
        :param page: The page number. Defaults to 1.
        :param page_size: The number of products to display per page. Defaults to 54.
        :param product_brand_id: An optional product brand ID to filter products by brand.
        :param sort_by: Sorting criteria. The possible value is: PROMO, populer, terbaru, alfabet(a-z), alfabet(z-a), harga terendah, harga tertinggi.
        :param start_price: Start price in rupiah
        :param end_price: End price in rupiah
        :param attributes: Attributes
        :param show_item: Specify the provider to use. 'TI' for Toko Indomaret or '26' for Warehouse Jakarta 1
        :param return_in_json: Return in JSON string or in list object
        :param print_log: Print link, number of page, and product result in python logging
        :return: JSON or object about the products in this category
        """
        page_url = self._category_query_builder(
            category_link, page, page_size, sort_by, product_brand_id, start_price, end_price, attributes, show_item
        )

        content = self.load_page(page_url, 'wrp-produk-list')
        soup: BeautifulSoup = BeautifulSoup(content, self.bs4_parser)

        if print_log:
            logging.info(page_url)

        product_result = decode_products(soup)

        if print_log:
            page_num = len(
                soup \
                    .find("select", class_="form-control pagelist") \
                    .find_all("option", recursive=False)
            )
            logging.info(f"Number Of Page: {page_num}")
            logging.debug(product_result)

        if return_in_json:
            return self.json_encoder.encode(product_result)
        else:
            return product_result

    def get_category_list(
            self,
            return_in_json: bool = True,
            print_log: bool = False,
    ):
        content = self.load_page(self.base_url, 'brand')
        soup: BeautifulSoup = BeautifulSoup(content, self.bs4_parser)

        category_result = decode_categories(soup)

        if print_log:
            logging.info("Getting Category List")
            logging.debug(category_result)

        if return_in_json:
            return self.json_encoder.encode(category_result)
        else:
            return category_result

    def _category_query_builder(
            self,
            category_link: str,
            page: int = 1,
            page_size: int = 54,
            sort_by: str = "PROMO",
            product_brand_id: str = None,
            start_price: int = None,
            end_price: int = None,
            attributes: str = None,
            show_item: str = None
    ) -> str:
        """
           Constructs a query URL string for category page of KlikIndomaret.

            :param category_link: Whole or part of the category page URL
            :param page: The page number. Defaults to 1.
            :param page_size: The number of products to display per page. Defaults to 54.
            :param product_brand_id: An optional product brand ID to filter products by brand.
            :param sort_by: The sorting criteria. The possible value is: `PROMO`, `populer`, `terbaru`, `alfabet(a-z)`,
            `alfabet(z-a)`, `harga terendah`, `harga tertinggi`. Defaults to `PROMO`
            :param start_price: Start price in rupiah
            :param end_price: End price in rupiah
            :param attributes: Attributes
            :param show_item: Specify the provider to use. `TI` for Toko Indomaret or `26` for Warehouse Jakarta 1
            :return: The complete URL with query parameters appended to the `category_link`
           """

        if category_link.find(self.base_url_no_https) == -1:
            if category_link[0] != "/":
                category_link = "/" + category_link
            category_link = self.base_url + category_link
        if category_link[-1] == '/':
            category_link = category_link[:-1]

        category = category_link.split(sep='/')[-1]

        query_string = f"?categories={category}"
        query_string += f"&productbrandid={str(product_brand_id or '')}"
        query_string += f"&sortcol={sort_by}&pageSize={page_size}&page={page}"
        query_string += f"&startprice={str(start_price or '')}"
        query_string += f"&endprice={str(end_price or '')}"
        query_string += f"&attributes={str(attributes or '')}"
        query_string += f"&ShowItem={str(show_item or '')}"

        return category_link + query_string

    def load_page(self, link: str, class_to_wait: str, wait_time=6):
        self.driver.get(link)

        self.wait_for_page(class_to_wait, wait_time)

        return self.driver.page_source

    def wait_for_page(self, class_to_wait: str, wait_time: int):
        try:
            wait = WebDriverWait(self.driver, timeout=wait_time)
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, class_to_wait)))
        except:
            raise LookupError("There is no element specified")
