import scrapy

class AsianspiderSpider(scrapy.Spider):
    name = "asianspider"
    allowed_domains = ["asyafanatiklerim.com"]
    start_urls = ["https://asyafanatiklerim.com/tur/macera","https://asyafanatiklerim.com/tur/romantik","https://asyafanatiklerim.com/tur/dram","https://asyafanatiklerim.com/tur/aile","https://asyafanatiklerim.com/tur/aksiyon","https://asyafanatiklerim.com/tur/fantastik","https://asyafanatiklerim.com/tur/genclik","https://asyafanatiklerim.com/tur/gerilim","https://asyafanatiklerim.com/tur/gizem","https://asyafanatiklerim.com/tur/hukuk","https://asyafanatiklerim.com/tur/komedi","https://asyafanatiklerim.com/tur/medikal","https://asyafanatiklerim.com/tur/polisiye","https://asyafanatiklerim.com/tur/tarih"]
    

    def parse(self, response):
        category = response.css('div.content')

        products = response.css('article')

        for product in products:
            if product.css('a::text').get() is None:
                continue

            yield {
                'category': category.css('header h1::text').get(),
                'name': product.css('a::text').get(),
                'rating': product.css('div.poster div.rating::text').get(),
                'year': product.css('div.data span').get().replace("<span>", "").replace("</span>", ""),
                'url': product.css('h3 a::attr(href)').get()
            }

        next_page = response.css('div.pagination a.arrow_pag:last-of-type').attrib.get('href')

        if next_page:  # next_page boş değilse, yani None değilse
            yield response.follow(next_page, callback=self.parse)

