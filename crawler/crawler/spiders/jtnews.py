import scrapy


class JtnewsSpider(scrapy.Spider):
    name = 'jtnews'
    allowed_domains = ['www.jtnews.jp']
    start_urls = ['http://www.jtnews.jp/']

    def parse(self, response):
        pass
