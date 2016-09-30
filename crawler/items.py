# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HabraparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ListItem(scrapy.Item):
    posts = scrapy.Field()


class PostItem(scrapy.Item):
    post_title = scrapy.Field()
    post_url = scrapy.Field()
    post_cut = scrapy.Field()


class HubItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    posts = scrapy.Field()
