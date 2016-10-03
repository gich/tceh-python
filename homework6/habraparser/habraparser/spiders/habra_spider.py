# -*- coding: utf-8 -*-

import re
import scrapy
from habraparser.items import PostItem, HubItem


class HabraSpider(scrapy.Spider):
    name = "Habr"

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'}

    def __init__(self, user_name=None, *args, **kwargs):
        super(HabraSpider, self).__init__(*args, **kwargs)
        self.url = "https://habrahabr.ru/users/{}/".format(user_name)

    def start_requests(self):
        yield scrapy.Request(url=self.url,
                             callback=self.parse,
                             errback=self.not_found_user)

    def not_found_user(self, response):
        raise NameError('User not found!')

    def parse(self, response):
        for l in response.css('ul#hubs_data_items>li'):
            hub = HubItem(hub_name=l.css('a ::text').extract_first(),
                          hub_url=l.css('a ::attr(href)').extract_first(),
                          hub_posts=[])
            new_parse = self.parse_posts(hub)
            follow_url = hub['hub_url']

            yield scrapy.Request(response.urljoin(follow_url),
                                 callback=new_parse)

    def parse_posts(self, hub):
        def parse_post_page(response):
            for p in response.css('div.post_teaser'):
                title = p.css('div.post__header > h2 > a::text'
                              ).extract_first()
                post_url = p.css('div.post__header > h2 >a ::attr(href)'
                                 ).extract_first()
                post_cut = p.css('div.post__body_crop>div.content ::text'
                                 ).extract_first()
                post_cut = re.sub(r'<.*?>', '', post_cut)
                item = PostItem(post_title=title,
                                post_url=post_url,
                                post_cut=post_cut
                                )
                hub['hub_posts'].append(item)

            return hub
        return parse_post_page




