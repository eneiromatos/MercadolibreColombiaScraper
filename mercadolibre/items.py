"""
Scraper For Mercadolibre Colombia: is designed to scrape products data 
from Mercadolibre' specific users.
Copyright (C) 2022. Eneiro A. Matos B.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
import re


def top_sales(value: str) -> bool:
    if "más vendido" in value.casefold():
        return True


def free_shipping(value: str) -> str:
    if value.casefold().strip() in ("llega gratis", "envío gratis a nivel nacional"):
        return True


def price_to_num(value: str) -> float:
    value = value.replace(".", "")
    return float(value)


def rating_to_num(value: str) -> float:
    return float(value)


def stock_to_num(value: str) -> int:
    return int(re.findall(r"[0-9]+", value)[0])


class MercadolibreItem(scrapy.Item):

    url = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(output_processor=TakeFirst())

    current_price = scrapy.Field(
        input_processor=MapCompose(price_to_num), output_processor=TakeFirst()
    )

    last_price = scrapy.Field(
        input_processor=MapCompose(price_to_num), output_processor=TakeFirst()
    )

    is_top_sales = scrapy.Field(
        input_processor=MapCompose(top_sales), output_processor=TakeFirst()
    )

    rating = scrapy.Field(
        input_processor=MapCompose(rating_to_num), output_processor=TakeFirst()
    )

    has_free_shipping = scrapy.Field(
        input_processor=MapCompose(free_shipping),
        output_processor=TakeFirst(),
    )

    in_stock = scrapy.Field(
        input_processor=MapCompose(stock_to_num), output_processor=TakeFirst()
    )


class MercasdolibreUserItem(scrapy.Item):

    username = scrapy.Field(output_processor=TakeFirst())

    user_url = scrapy.Field(output_processor=TakeFirst())

    leader_status = scrapy.Field(output_processor=TakeFirst())

    date_time = scrapy.Field(output_processor=TakeFirst())
