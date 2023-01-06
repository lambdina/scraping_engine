import random

import scrapy

from scraping_engine.items import PaperItem, AuthorItem
from scraping_engine.utils import clear_join


class NatureSpider(scrapy.Spider):
    name = "nature"
    start_urls = [
        "https://www.nature.com/nature/research-articles"
    ]
    domain = "nature.com"

    def parse(self, response):
        css_selector = "li.app-article-list-row__item"
        item_positions = [i for i in range(len(response.css(css_selector)))]
        while len(item_positions) > 0:
            pos = random.choice(item_positions)
            idx = item_positions.index(pos)
            item_positions.remove(pos)

            article = response.css(css_selector)[idx]
            name = clear_join(article.css("h3 ::text").getall())
            detail_link = f'https://{self.domain}{article.css("a ::attr(href)").get()}'
            release_date = article.css('time[itemprop="datePublished"] ::attr(datetime)').get()

            yield scrapy.Request(detail_link, self.parse_publishing_house, meta={
                "name": name,
                "detail_link": detail_link,
                "release_date": release_date
            })


    def get_university_name(self, lab_info: list) -> str:
        for info in lab_info:
            if 'University' in info:
                return info
        return ""


    def parse_publishing_house(self, response):
        item = PaperItem()
        item["name"] = response.meta.get("name")
        item["detail_link"] = response.meta.get("detail_link")
        item["release_date"] = response.meta.get("release_date")
        item["abstract"] = clear_join(response.css('div[id="Abs1-content"] ::text').getall())
        item["topics"] = response.css(".c-article-subject-list li ::text").getall()
        yield item
        
        for lab in response.css('div[id="author-information-content"] .c-article-author-affiliation__list li'):
            lab_info = lab.css('.c-article-author-affiliation__address ::text').get().split(", ")
            for author in lab.css(".c-article-author-affiliation__authors-list ::text").getall():
                complete_name = author.split(" ")
                item = AuthorItem()
                item["paper_name"] = response.meta.get("name")
                item["paper_release_date"] = response.meta.get("release_date")
                item["first_name"] = complete_name[0]
                item["last_name"] = complete_name[-1]
                item["laboratory_name"] = lab_info[0]
                item["laboratory_university"] = self.get_university_name(lab_info)
                item["laboratory_location"] = lab_info[-1]
                yield item

