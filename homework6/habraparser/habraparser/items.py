# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def serialize_str(value):
    return value.__repr__()


class HabraparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PostItem(scrapy.Item):
    post_title = scrapy.Field()
    post_url = scrapy.Field()
    post_cut = scrapy.Field()


class HubItem(scrapy.Item):
    hub_name = scrapy.Field() # serializer=serialize_str)
    hub_url = scrapy.Field()
    hub_posts = scrapy.Field()
