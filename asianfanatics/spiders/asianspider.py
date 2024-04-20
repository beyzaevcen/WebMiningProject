import scrapy


class AsianspiderSpider(scrapy.Spider):
    name = "asianspider"
    allowed_domains = ["asyafanatiklerim.com"]
    start_urls = ["https://asyafanatiklerim.com/tur/romantik/"]

    def parse(self, response):
        products = response.css('article')

        for product in products:

            yield{
                'name': product.css('a::text').get(),
                'rating': product.css('div.rating').get().replace('<div class="rating"><span class="icon-star2"></span> ','' ).replace('</div>',''),
                'year': product.css('div.data span').get().replace("<span>", "").replace("</span>", "") ,
                'url': product.css('h3 a').attrib['href']
            }

