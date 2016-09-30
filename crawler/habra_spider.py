# -*- coding: utf-8 -*-


import scrapy
from habraparser.items import PostItem, HubItem, ListItem


class HabraSpider(scrapy.Spider):
    name = "Habr"

    def start_requests(self):
        url = "https://habrahabr.ru/users/lexxxander/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for l in response.css('ul#hubs_data_items>li'):
            hub = HubItem(name=l.css('a ::text').extract_first(),
                          url=l.css('a ::attr(href)').extract_first())
            # yield hub
            follow_url = hub['url']

            yield scrapy.Request(response.urljoin(follow_url),
                                       callback=self.parse_posts)

            print('Wait for it!')

    def parse_posts(self, response):
        l = ListItem()
        l['posts'] = []
        for p in response.css('div.post_teaser'):
                # css('h2.post__title'):

            l['posts'].append(PostItem(post_title=p.css(
                'div.post__header > h2 > a::text').extract_first(),
                           post_url=p.css(
                'div.post__header > h2 >a ::attr(href)').extract_first(),
                           post_cut=p.css(
                'div.post__body_crop>div.buttons>a ::attr(href)').extract_first())
                           )
        return l



