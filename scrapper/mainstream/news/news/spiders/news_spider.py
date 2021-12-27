
from .parsed_news_model import ParsedNewsModel
import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import csv
import html2text

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = [
        "detik.com",
    ]
    start_urls = [
        "https://www.detik.com/tag/banjir",
        "https://www.detik.com/tag/gempa",
    ]
    interator = 0

    def __init__(self, *a, **kw):
        super(NewsSpider, self).__init__(*a, **kw)
        f = open('scrapped_news.csv', 'w')

        writer = csv.writer(f)
        writer.writerow(['title', 'description', 'date'])

        f.close()

    def parse(self, response):
        domain = urlparse(response.request.url).netloc

        if (domain == "www.detik.com"):
            for article in response.css("article"):
                link = article.css("a::attr(href)").extract_first()

                yield response.follow(link, self.parse_article)

            for navbutton in response.css('a'):
                if self.interator == 2:
                    break

                if navbutton.css("a.last img::attr(alt)").extract_first() == "Kanan":
                    next_page = navbutton.css(
                        "a.last::attr(href)").extract_first()
                    if next_page is not None:
                        self.interator += 1
                        next_page = response.urljoin(next_page)
                        yield scrapy.Request(next_page, callback=self.parse)

    def parse_article(self, response):
        f = open('scrapped_news.csv', 'a')

        desc = ""
        newsModel = ParsedNewsModel()

        title = response.css("h1.detail__title::text").extract_first()
        newsModel.title = ""
        

        if title != None:
            date = response.css("div.detail__date::text").extract_first()
            desc += self.textParser(title)
            newsModel.title = self.textParser(title)
            newsModel.date = self.textParser(date)
        else:
            title = response.css("h1.mt5::text").extract_first()
            date = response.css("div.date::text").extract_first()
            newsModel.title = self.textParser(title)
            newsModel.date = self.textParser(date)

        for paragraph in response.css('p'):
          paragraphBody = paragraph.css("p::text").extract_first()
          if paragraphBody != None:
            desc += (self.textParser(paragraphBody) + " ")

        newsModel.description = desc
        
        writer = csv.writer(f)
        writer.writerow([str(newsModel.title), str(newsModel.description), str(newsModel.date)])

        f.close()

    def textParser(self, text):
        converter = html2text.HTML2Text()
        converter.ignore_links = True

        return converter.handle(text)