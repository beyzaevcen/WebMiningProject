import scrapy
import numpy as np
import time
import random


class YearsspiderSpider(scrapy.Spider):
    name = "yearsspider"
    allowed_domains = ["asyafanatiklerim.com"]
    bases = np.arange(2010, 2025)
    #start_urls = ["https://asyafanatiklerim.com/yil/2010/"]


    def start_requests(self):
        url = "https://asyafanatiklerim.com/yil/"
        for base in self.bases:
            wait_time = random.uniform(3, 5)
            time.sleep(wait_time)
            yield scrapy.Request(url + str(base), callback=self.parse)

    def parse(self, response):
        products = response.css('article')

        for product in products:
            item_name = product.css('a::text').get() 
            if not item_name:
                continue

            yield {
                'name': product.css('a::text').get(),
                'rating': product.css('div.poster div.rating::text').get(),
                'year': product.css('div.data h3 + span::text').get(),
                'url': product.css('h3 a::attr(href)').get()
            }

        next_page = response.css('div.pagination a.arrow_pag:last-of-type').attrib.get('href')
        next_pages = response.css('div.pagination a.inactive::attr(href)').getall()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            for next_page2 in next_pages:
                yield response.follow(next_page2, callback=self.parse)

