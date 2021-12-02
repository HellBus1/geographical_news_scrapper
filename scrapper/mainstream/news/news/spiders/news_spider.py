import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["detik.com"]
    start_urls = [
        "https://www.detik.com/search/searchall?query=bencana&siteid=2",
    ]
    interator = 0

    def parse(self, response):
        for article in response.css("article"):
            link = article.css("a::attr(href)").extract_first()

            yield response.follow(link, self.parse_article)

        for navbutton in response.css('a'):
            if self.interator == 10:
                break

            if navbutton.css("a.last img::attr(alt)").extract_first() == "Kanan":
                next_page = navbutton.css(
                    "a.last::attr(href)").extract_first()
                if next_page is not None:
                    self.interator += 1
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)

    def parse_article(self, response):
        print(response.css("title").extract_first())
        print("")
