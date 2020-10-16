# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewItem(scrapy.Item):
    point = scrapy.Field(serializer=int)
    movie_id = scrapy.Field(serializer=int)
    user_id = scrapy.Field(serializer=int)


class UserItem(scrapy.Item):
    user_id = scrapy.Field(serializer=int)
    name = scrapy.Field(serializer=str)


class MovieItem(scrapy.Item):
    movie_id = scrapy.Field(serializer=int)
    title = scrapy.Field(serializer=str)
