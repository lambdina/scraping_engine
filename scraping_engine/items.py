# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikipediaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    publishing_house_name = scrapy.Field()
    dns_names = scrapy.Field()

class AuthorItem(scrapy.Item):
    paper_name = scrapy.Field()
    paper_release_date = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    laboratory_name = scrapy.Field()
    laboratory_university = scrapy.Field()
    laboratory_location = scrapy.Field()


class PaperItem(scrapy.Item):
    name = scrapy.Field()
    release_date = scrapy.Field()
    abstract = scrapy.Field()
    topics = scrapy.Field()
    detail_link = scrapy.Field()

