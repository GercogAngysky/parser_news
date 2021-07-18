# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Russia24Item(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    datetime = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    source_link = scrapy.Field()
    image = scrapy.Field()
    text = scrapy.Field()