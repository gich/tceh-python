import scrapy


class HabraSpider(scrapy.Spider):
    name = "Habr"

    def start_requests(self):
        url = "https://habrahabr.ru/users/lexxxander/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse_posts(self, response):
        posts = []
        for p in response.css('h2.post__title'):
            posts.append({'post_title': p.css('a::text').extract_first()})
        return {'all_posts': posts}

    def parse(self, response):
        for l in response.css('ul#hubs_data_items>li'):
            result = {'hubname': l.css('a ::text').extract_first(),
                      'hub_url': l.css('a ::attr(href)').extract_first(),
                      'hub_posts': []}
            follow_url = result['hub_url']
            posts = scrapy.Request(response.urljoin(follow_url),
                                         callback=self.parse_posts)
            result['hub_posts'].append(posts['all_posts'])
            print('Wait for it!')
            print(result)
