# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieReviewCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    body = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    url_md5 = scrapy.Field()
    created_at = scrapy.Field()
    meta = scrapy.Field()
    summary_image = scrapy.Field()
