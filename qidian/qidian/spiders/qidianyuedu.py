import scrapy
from qidian.items import QidianItem

class QidianyueduSpider(scrapy.Spider):
    name = 'qidianyuedu'
    allowed_domains = ['book.qidian.com']
    start_urls = ['http://qidian.com/']

    def start_requests(self):
        # page_num = self.get_page_num()
        page_num = 10
        for i in range(1, page_num + 1):
            url = "https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=" \
                        + str(i)
            yield scrapy.Request(url,
                                 callback=self.parse,
                                 headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                        "Chrome/63.0.3239.132 Safari/537.36"})

    def parse(self, response):
        li_list = response.css(".book-img-text li")
        for li in li_list:
            item = QidianItem()
            item["title"] = li.css(".book-mid-info h4 a::text")[0].extract()
            item["url"] = "https:" + li.css(".book-mid-info h4 a::attr(href)")[0].extract()
            item["author"] = li.css(".book-mid-info .author a")[0].xpath("./text()")[0].extract()
            category = ""
            a_list = li.css(".book-mid-info .author a")[1:]
            for a in a_list:
                a_text = a.css("a::text")[0].extract()
                category += a_text
                category += " "
            item["category"] = category.strip()
            item["status"] = li.css(".book-mid-info .author span::text")[0].extract()
            item["bref"] = li.css(".book-mid-info .intro::text")[0].extract().strip()

            yield scrapy.Request(item['url'],
                                 callback=self.book_intro,
                                 meta={"item": item},
                                 headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                        "Chrome/63.0.3239.132 Safari/537.36"})

    def book_intro(self,response):
        import bs4
        item = response.meta["item"]
        doc = bs4.BeautifulSoup(response.text, 'lxml')
        item["bref"] = doc.find("div",class_="book-intro").find("p").text.strip('')\
                                .replace(u"\u3000", u'').replace("\r", '').replace("\n", '').replace(" ", '')
        yield item



