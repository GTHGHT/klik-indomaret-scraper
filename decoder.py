from bs4 import BeautifulSoup, Tag, ResultSet

from util import rupiah_str_to_int


def decode_categories(bs: BeautifulSoup):
    cat_result = []

    cat_section_tag: Tag = bs.body.find('ul', id="headerMobileChannel")
    super_cat_rs: ResultSet = cat_section_tag \
        .find_all('li', attrs={"class": "kategori", "data-name": None})

    for super_cat_tag in super_cat_rs:
        cat_info = []

        cat_header: str = super_cat_tag.find('span', class_="clickMenu").contents[0]
        cat_rs: ResultSet = super_cat_tag \
            .find("ul", class_="wrp-submenu st-kategori") \
            .find_all("li", class_=None, recursive=False)

        for cat in cat_rs:
            cat_dict = {}

            cat_name: Tag = cat.find("span", class_="clickMenu", recursive=False)

            if type(cat_name.contents[0]) is Tag:
                cat_dict["category_name"] = cat_name.string
                cat_dict["link"] = cat_name.find("a")["href"]
                cat_info.append(cat_dict)
                continue

            cat_link: str = cat.find("li", class_="menu-seeall").find("a")["href"]

            subcat_rs: ResultSet = cat.find(
                "ul",
                class_="nd-kategori",
                recursive=False
            ).find_all(
                "a",
                onclick="clickTrackerCATS(this,'', 0, 'Kategori', false)"
            )

            cat_dict["category_name"] = cat_name.string
            cat_dict["link"] = cat_link
            cat_dict["subcategories"] = [" ".join(subcat.string.split()) for subcat in subcat_rs]
            cat_info.append(cat_dict)

        super_cat_dict = dict(super_category=cat_header, categories=cat_info)
        cat_result.append(super_cat_dict)
    return cat_result


def decode_products(bs: BeautifulSoup):
    products_result = []
    body_bs: Tag = bs.body
    products_rs: ResultSet = body_bs.find(
        'div',
        class_="product-collection"
    ).find_all(
        'div',
        class_="item",
        recursive=False
    )

    product_category: str = body_bs \
        .find("div", class_="breadcrumb") \
        .select_one("a:last-child").string

    for product_tag in products_rs:
        product_dict = dict()
        old_price: Tag | None = product_tag.find('span', class_="strikeout")
        discount: Tag | None = product_tag.find('span', class_="discount")
        normal_price: str = product_tag.find('span', class_="normal").string.strip()
        is_discount = False
        product_dict["plu"] = product_tag['data-plu']
        product_dict["link"] = "https://www.klikindomaret.com" + product_tag.find('a')['href']
        product_dict["title"] = product_tag.find('div', class_="title").string.strip()
        product_dict["category"] = " ".join(product_category.split())
        product_dict["price"] = rupiah_str_to_int(normal_price)
        if old_price is not None:
            product_dict["old_price"] = rupiah_str_to_int(old_price.contents[-1].strip())
        if discount is not None:
            is_discount = True
            product_dict["discount"] = discount.string.strip()
        product_dict["is_discount"] = is_discount
        product_dict["is_flash_sale"] = product_tag.find('div', class_="flash-product") is not None
        products_result.append(product_dict)
    return products_result
