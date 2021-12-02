import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class DetikSpider(scrapy.Spider):
    name = "detik"
    allowed_domains = ["detik.com"]
    start_urls = [
        "https://www.detik.com/search/searchall?query=bencana&siteid=2",
    ]

    def parse(self, response):
        for article in response.css("article"):
            link = article.css("a::attr(href)").extract_first()

            yield response.follow(link, self.parse_article)

        next_page = response.xpath('a.last').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        for text in response.css("div.detail__body-text"):
            print(text.css("p").extract_first())
