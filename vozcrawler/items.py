# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VozcrawlerItem(scrapy.Item):
    comment_id = scrapy.Field()
    comment_content = scrapy.Field()

    images = scrapy.Field()
    image_urls = scrapy.Field()