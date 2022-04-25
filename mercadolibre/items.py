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


def top_sales(value: str) -> bool:
    if value is not None:
        return True


def free_shipping(value: str) -> str:
    if value is not None:
        return True


def price_to_num(value: str) -> float:
    value = value.replace(".", "")
    return float(value)


def rating_to_num(value: str) -> float:
    return float(value)


class MercadolibreItem(scrapy.Item):

    url = scrapy.Field(output_processor=TakeFirst())

    title = scrapy.Field(output_processor=TakeFirst())

    price = scrapy.Field(
        input_processor=MapCompose(price_to_num), output_processor=TakeFirst()
    )

    is_top_sales = scrapy.Field(
        input_processor=MapCompose(top_sales), output_processor=TakeFirst()
    )

    rating = scrapy.Field(
        input_processor=MapCompose(rating_to_num), output_processor=TakeFirst()
    )

    has_free_shipping = scrapy.Field(
        input_processor=MapCompose(free_shipping), output_processor=TakeFirst()
    )
