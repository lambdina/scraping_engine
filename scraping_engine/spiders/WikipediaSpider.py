import scrapy
import re

from scraping_engine.items import WikipediaItem


class QuotesSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Maison_d%27%C3%A9dition_d%27ouvrages_scientifiques',
    ]
    domain = "fr.wikipedia.org"

    def parse(self, response):
        for publishing_house in response.css(".mw-category-group li"):
            link = publishing_house.css("a ::attr(href)").get()
            yield scrapy.Request(f'https://{self.domain}{link}', callback=self.parse_publishing_house)

    def parse_publishing_house(self, response):
        item = WikipediaItem()
        item["publishing_house_name"] = response.css("h1 ::text").get()
        dns_pattern = "^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"
        url_pattern = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        dns_names = []
        for row in response.css("a ::text").getall():
            if "https://fr.wikipedia.org/w/index.php" in row:
                continue
            if re.match(dns_pattern, row):
                dns_names.append(row)
            elif re.match(url_pattern, row):
                dns_names.append(row)
        item["dns_names"] = dns_names
        yield item

            