
import string
from .parsed_news_model import ParsedNewsModel
import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import html2text
import logging
from scrapy.utils.log import configure_logging
import pandas as pd
from scrapy import signals
from pydispatch import dispatcher

class NewsSpider(scrapy.Spider):
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )        

    name = "news"
    allowed_domains = [
        "detik.com",
        "kompas.com",
        "tribunnews.com"
    ]
    start_urls = [
        # "https://www.detik.com/tag/bencana",
        "https://www.detik.com/tag/gempa",
        # "https://www.detik.com/tag/banjir",
        # "https://www.detik.com/tag/banjir-bandang",
        "https://www.detik.com/tag/kemarau",
        "https://www.detik.com/tag/kekeringan",
        "https://www.detik.com/tag/kebakaran-hutan",
        "https://www.detik.com/tag/cuaca-panas",
        "https://www.detik.com/tag/awan-panas",
        "https://www.detik.com/tag/longsor",
        "https://www.detik.com/tag/angin-kencang",
        "https://www.detik.com/tag/bencana-alam",
        "https://www.detik.com/tag/pergerakan-tanah",
        "https://www.detik.com/tag/pergeseran-tanah",
        "https://www.detik.com/tag/kebakaran",
        "https://www.detik.com/tag/erosi",
        "https://www.detik.com/tag/abrasi",
        "https://www.detik.com/tag/tsunami",
        # "https://www.kompas.com/tag/kecelakaan"
        # "https://www.kompas.com/tag/bencana",
        # "https://www.tribunnews.com/tag/bencana"
    ]
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    interator = 0
    current_domain = ""
    current_url = ""
    berita = []
    visited = []

    def __init__(self, *a, **kw):
        super(NewsSpider, self).__init__(*a, **kw)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        domain = urlparse(response.request.url).netloc
        if self.current_url != response.request.url:
            self.current_url = response.request.url
            self.visited.clear()

        if (domain == "www.detik.com"):
            self.current_domain = domain
            for article in response.css("article"):
                link = article.css("a::attr(href)").extract_first()

                yield response.follow(link, self.parse_detik)

            for navbutton in response.css('div.paging a'):
                
                currentIndexView = navbutton.css("a::text").extract_first()
                if currentIndexView != None:
                    if (currentIndexView.isnumeric() and (currentIndexView not in self.visited)):
                        self.visited.append(currentIndexView)
                        next_page = navbutton.css("a::attr(href)").extract_first()
                        
                        if next_page is not None and ("tv." not in next_page):
                            next_page = response.urljoin(next_page)
                            yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)

                elif "next" in navbutton.css("a::attr(onclick)").extract_first():    
                    next_page = navbutton.css("a::attr(href)").extract_first()
                    if next_page is not None and ("tv." not in next_page):
                        self.interator += 1
                        next_page = response.urljoin(next_page)
                        yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)

        elif (domain == "www.kompas.com"):
            self.current_domain = domain
            for article in response.css("div.article__list"):
                link = article.css("a::attr(href)").extract_first() 
                # + "?page=all"

                yield response.follow(link, self.parse_kompas)

                next_page = response.css(
                    "a.paging__link--next::attr(href)").extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)

        elif (domain == "www.tribunnews.com"):
            self.current_domain = domain
            for article in response.css("ul.lsi"):
                link = article.css("a::attr(href)").extract_first() + "?page=all"

                yield response.follow(link, self.parse_tribun)

            for navbutton in response.css('div.paging a'):
                if navbutton.css("a::text").extract_first() == "Next":
                    
                    next_page = navbutton.css("a::attr(href)").extract_first()

                    if next_page is not None:
                        self.interator += 1
                        next_page = response.urljoin(next_page)
                        yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)

    def parse_kompas(self, response):
        desc = ""

        title = response.css("h1.read__title::text").extract_first()

        date = response.css("div.read__time::text").extract_first()

        title = self.textParser(title)
        date = self.textParser(date)

        for paragraph in response.css("div.read__content p"):
            paragraphBody = paragraph.css("p::text").extract_first()
            if paragraphBody != None:
                desc += (self.textParser(paragraphBody) + " ")

        description = desc
        if description != "" and title != "" and date != "":
            data = [str(title), str(date), str(description), str(self.current_domain)]

            self.berita.append(data)

    def parse_detik(self, response):
            
        author = response.css("div.detail__author::text").extract_first()
        
        desc = ""

        title = response.css("h1.detail__title::text").extract_first()

        if title != None:
            date = response.css("div.detail__date::text").extract_first()
        else:
            title = response.css("h1.mt5::text").extract_first()
            date = response.css("div.date::text").extract_first()
            
        title = title
        date = date
        date = date

        # if len(response.css('p')) > 0 :
        for paragraph in response.css('p'):
            paragraphBody = paragraph.css("p::text").extract_first()
            if paragraphBody != None:
                desc += (self.textParser(paragraphBody) + " ")

        description = desc
        
        if description != "" and title != "" and date != "":
            data = [str(title), str(date), str(description), str(self.current_domain)]

            self.berita.append(data)
    
    def parse_tribun(self, response):
        desc = ""

        title = response.css("#arttitle::text").extract_first()

        date = response.css("time::text").extract_first()

        title = self.textParser(title)
        date = self.textParser(date)

        for paragraph in response.css("div.txt-article p"):
            paragraphBody = paragraph.css("p::text").extract_first()
            if paragraphBody != None:
                desc += (self.textParser(paragraphBody) + " ")

        description = desc
        if description != "" and title != "" and date != "":
            data = [str(title), str(date), str(description), str(self.current_domain)]

            self.berita.append(data)

    def spider_closed(self, spider):
        writer = pd.DataFrame(self.berita, columns=['title', 'date', 'description', 'source'])
        writer.to_csv('scrapped_news.csv', index=False, sep=',')

    def textParser(self, text):
        converter = html2text.HTML2Text()
        converter.ignore_links = True

        return converter.handle(text)
