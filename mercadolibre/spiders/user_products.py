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
from ..items import MercadolibreItem
from scrapy.loader import ItemLoader


class UserProductsSpider(scrapy.Spider):
    name = "user_products"
    allowed_domains = [
        "www.mercadolibre.com.co",
        "listado.mercadolibre.com.co",
        "articulo.mercadolibre.com.co",
    ]

    headers = {
        "authority": "www.mercadolibre.com.co",
        "cache-control": "max-age=0",
        "device-memory": "8",
        "dpr": "1",
        "viewport-width": "1366",
        "rtt": "250",
        "downlink": "9.6",
        "ect": "4g",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "dnt": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": "https://www.mercadolibre.com.co/bascula-xiaomi-mi-body-composition-scale-2-blanca-hasta-150-kg/p/MCO15280499?pdp_filters=seller_id:193394280",
        "accept-language": "es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
        "cookie": '_csrf=ffqj9vZjjVDwGphPF8dXMZNo; c_ui-navigation=5.18.9; _d2id=ce83796f-924d-4015-aa77-5f1c8fa31091; tooltips-configuration={"highlight_api_tooltip":{"view_cnt":1,"close_cnt":0,"view_time":1650825902,"close_time":0}}; cookiesPreferencesNotLogged=%7B%22categories%22%3A%7B%22advertising%22%3Atrue%7D%7D; onboarding_cp=false; LAST_SEARCH=cesta; c_seller=1.0.0-nordic782-1; navigation_items=MCO870953811%7C24042022223641%7CMCO15280499%7CMCO10419851-MCO856224815%7C24042022210639-MCO580597467%7C24042022205920-MCO881132953%7C24042022205239-MCO882434065%7C24042022205220; _d2id=e59fa8c8-8b3e-4d60-9a3e-2429053bd00a-n',
    }

    def start_requests(self):
        url = f"https://www.mercadolibre.com.co/perfil/{self.user}"
        yield scrapy.Request(url, self.parse, headers=self.headers)

    def parse(self, response):
        products_page = response.css("a.publications__subtitle::attr(href)").get()
        yield response.follow(
            products_page, self.parse_products_list, headers=self.headers
        )

    def parse_products_list(self, response, **kwargs):
        products_list = response.css("li.ui-search-layout__item")
        products_urls = products_list.css(
            'div[class="ui-search-item__group ui-search-item__group--title"] a::attr(href)'
        ).getall()

        yield from response.follow_all(
            products_urls, self.parse_product_detail, headers=self.headers
        )

        next_page = response.css('a[title="Siguiente"]::attr(href)').getall()
        yield from response.follow_all(
            next_page, self.parse_products_list, headers=self.headers
        )

    def parse_product_detail(self, response, **kwargs):
        article = ItemLoader(MercadolibreItem(), response)
        article.add_value("url", response.url)
        article.add_css("title", "h1.ui-pdp-title::text")
        article.add_css(
            "last_price",
            's[class="andes-money-amount ui-pdp-price__part ui-pdp-price__original-value andes-money-amount--previous andes-money-amount--cents-superscript andes-money-amount--compact"] span.andes-money-amount__fraction::text',
        )
        article.add_css(
            "current_price",
            "div.ui-pdp-price__second-line span.andes-money-amount__fraction::text",
        )
        article.add_css("is_top_sales", "a.ui-pdp-promotions-pill-label__target::text")
        article.add_css("rating", "p.ui-pdp-reviews__rating__summary__average::text")
        article.add_css(
            "has_free_shipping",
            'svg[class="ui-pdp-icon ui-pdp-icon--shipping ui-pdp-icon--truck ui-pdp-color--GREEN"]::attr(class)',
        )
        article.add_css("in_stock", "span.ui-pdp-buybox__quantity__available::text")

        yield article.load_item()
