from selenium import webdriver

from scrapper import SeleniumKlikIndomaretScrapper
from util import save_json_to_file
import logging

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='running.log', encoding='utf-8', level=logging.INFO,
                        format='%(levelname)s:%(asctime)s | %(message)s')
    try:
        category = "/category/alat-kontrasepsi"
        page_num = 1
        page_size = 54

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)

        indomaret_scrapper = SeleniumKlikIndomaretScrapper(browser)
        logger.info(f"Getting {category} page {page_num}")

        product_json = indomaret_scrapper.get_products_from_category(category, page=page_num, page_size=page_size,
                                                                     return_in_json=False, print_log=True)
        logger.info(f"Saving JSON Result To {category.split(sep='/')[-1] + str(page_num) + '.json'}")

        save_json_to_file(product_json, 'hasil', category.split(sep='/')[-1] + str(page_num) + ".json")
        browser.quit()
    except Exception as e:
        logger.error(e)
