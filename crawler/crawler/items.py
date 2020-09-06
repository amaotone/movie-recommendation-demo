# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewItem(scrapy.Item):
    point = scrapy.Field()
    movie_id = scrapy.Field()
    user_id = scrpay.Field()


class UserItem(scrapy.Item):
    user_id = scrapy.Field()
    name = scrapy.Field()


class MovieItem(scrapy.Item):
    movie_id = scrapy.Field()
    title = scrapy.Field()
