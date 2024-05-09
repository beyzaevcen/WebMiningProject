import scrapy

class AsianspiderSpider(scrapy.Spider):
    name = "asianspider"
    allowed_domains = ["asyafanatiklerim.com"]

    #start_urls = ["https://asyafanatiklerim.com/tur/macera","https://asyafanatiklerim.com/tur/romantik","https://asyafanatiklerim.com/tur/dram","https://asyafanatiklerim.com/tur/aile","https://asyafanatiklerim.com/tur/aksiyon","https://asyafanatiklerim.com/tur/fantastik","https://asyafanatiklerim.com/tur/genclik","https://asyafanatiklerim.com/tur/gerilim","https://asyafanatiklerim.com/tur/gizem","https://asyafanatiklerim.com/tur/hukuk","https://asyafanatiklerim.com/tur/komedi","https://asyafanatiklerim.com/tur/medikal","https://asyafanatiklerim.com/tur/polisiye","https://asyafanatiklerim.com/tur/tarih"]
    

    types = ["hukuk", "romantik", "macera", "aile"]
    start_urls = ["https://asyafanatiklerim.com/tur/" + type_value for type_value in types]


    def parse(self, response):
        category = response.css('div.content')

        products = response.css('article')

       

        for product in products:
            item_name = product.css('a::text').get() 
            if not item_name:
                continue

            yield {
                'category': category.css('header h1::text').get(),
                'name': product.css('a::text').get(),

                'rating': product.css('div.poster div.rating::text').get(),
                'year': product.css('div.data span').get().replace("<span>", "").replace("</span>", ""),
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

        next_page = response.css('div.pagination a.arrow_pag:last-of-type').attrib.get('href')

        if next_page:  # next_page boş değilse, yani None değilse
            yield response.follow(next_page, callback=self.parse)

