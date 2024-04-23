import scrapy


class AsianspiderSpider(scrapy.Spider):
    name = "asianspider"
    allowed_domains = ["asyafanatiklerim.com"]
    start_urls = ["https://asyafanatiklerim.com/tur/romantik"]

    def parse(self, response):
        products = response.css('article')

       

        for product in products:

            yield{
                'name': product.css('a::text').get(),
                #'rating': product.css('div.rating').get().replace('<div class="rating"><span class="icon-star2"></span> ','' ).replace('</div>',''),
                'rating': product.css('div.poster div.rating::text').get(),
                'year': product.css('div.data span').get().replace("<span>", "").replace("</span>", "") ,
                #'year': product.css('div.data span.wdate::text').get(),
                'url': product.css('h3 a::attr(href)').get()
            }
        next_page = response.css('div.pagination a.arrow_pag:last-of-type').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)

        # next_page =  response.css('div.pagination a.arrow_pag').attrib.get('href')

        # if next_page is not None:
        #     next_page_url = response.urljoin(next_page)
        #     #next_page_url = "https://asyafanatiklerim.com" + next_page
        #     yield response.Request(next_page_url, callback = self.parse)

