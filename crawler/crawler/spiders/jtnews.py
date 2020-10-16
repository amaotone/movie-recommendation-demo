import scrapy
import re
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import time
from crawler.items import ReviewItem, UserItem, MovieItem
import logging


class JtnewsSpider(CrawlSpider):
    name = "jtnews"
    allowed_domains = ["www.jtnews.jp"]
    start_urls = ["https://www.jtnews.jp/cgi-bin_o/revlist.cgi?PAGE_NO=1"]

    rules = (
        Rule(
            LinkExtractor(allow=r"revlist\.cgi\?&?PAGE_NO=\d+$"),
            callback="parse_user",
            follow=True,
        ),
        Rule(
            LinkExtractor(allow=r"revper\.cgi\?&?REVPER_NO=\d+$"),
            follow=True,
        ),
        Rule(
            LinkExtractor(allow=r"revper\.cgi\?&?PAGE_NO=\d+&REVPER_NO=\d+&TYPE=1$"),
            callback="parse_review",
        ),
    )

    user_pattern = re.compile(r"REVPER_NO=(?P<user_id>\d+)")
    movie_pattern = re.compile(r"TITLE_NO=(?P<movie_id>\d+)")

    def parse_user(self, response):
        try:
            user_table = response.css("table")[-1]
            for link in user_table.css("a"):
                user = UserItem()
                user_url = link.css("a::attr(href)").get()
                user["user_id"] = int(self.user_pattern.findall(user_url)[0])
                user["name"] = link.css("a::text").get()
                yield user

        except:
            self.log(f"parse failed: {response.url}", level=logging.ERROR)
            yield scrapy.Request(
                response.url, callback=self.parse_user, dont_filter=True
            )

    def parse_review(self, response):
        # レビューの表は15番目で、1行目はヘッダーなので省く
        review_table = response.xpath("//th[contains(., '邦題')]/../..")
        user_id = int(self.user_pattern.findall(response.url)[0])
        if not review_table:
            return
        for row in review_table[0].css("tr")[1:]:
            movie = MovieItem()
            review = ReviewItem()

            cols = row.css("td")

            movie_url = cols[0].css("a::attr(href)").get()
            movie_id = int(self.movie_pattern.findall(movie_url)[0])
            movie["movie_id"] = movie_id
            movie["title"] = cols[0].css("a::text").get()

            review["point"] = int(cols[1].css("::text").get())
            review["movie_id"] = movie_id
            review["user_id"] = user_id

            yield movie
            yield review
