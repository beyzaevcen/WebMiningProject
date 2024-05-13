import scrapy


class TypesSpider(scrapy.Spider):
    name = "types"
    allowed_domains = ["asyafanatiklerim.com"]
    start_urls = ["https://asyafanatiklerim.com/tur/macera","https://asyafanatiklerim.com/tur/romantik","https://asyafanatiklerim.com/tur/dram","https://asyafanatiklerim.com/tur/aile","https://asyafanatiklerim.com/tur/aksiyon","https://asyafanatiklerim.com/tur/fantastik","https://asyafanatiklerim.com/tur/genclik","https://asyafanatiklerim.com/tur/gerilim","https://asyafanatiklerim.com/tur/gizem","https://asyafanatiklerim.com/tur/hukuk","https://asyafanatiklerim.com/tur/komedi","https://asyafanatiklerim.com/tur/medikal","https://asyafanatiklerim.com/tur/polisiye","https://asyafanatiklerim.com/tur/tarih"]
    
   
    already_scraped = set()

    def parse(self, response):
     
        category_name = response.url.split('/')[-1]
  
        if category_name not in self.already_scraped:
     
            yield {
                'category': category_name,
            }
  
            self.already_scraped.add(category_name)

        next_page = response.css('div.pagination a.arrow_pag:last-of-type').attrib.get('href')
        if next_page:
            yield response.follow(next_page, callback=self.parse)




import scrapy
from asianfanatics.items import AsianSeries
import pandas as pd
import numpy as np


class YearsspiderSpider(scrapy.Spider):
    name = "yearsspider"
    allowed_domains = ["asyafanatiklerim.com"]
    bases = np.arange(2010, 2025)
    #start_urls = ["https://asyafanatiklerim.com/yil/2010/"]


    def start_requests(self):
        url = "https://asyafanatiklerim.com/yil/"
        for base in self.bases:
            yield scrapy.Request(url + str(base), callback=self.parse)

    def parse(self, response):
        products = response.css('article')

        product_item = AsianSeries()

        for product in products:
            item_name = product.css('a::text').get() 
            if not item_name:
                continue

            product_item['name'] = product.css('a::text').get(),
            product_item["rating"] = product.css('div.poster div.rating::text').get(),
            product_item["year"] = product.css('div.data h3 + span::text').get().replace("<span>", "").replace("</span>", ""),
            product_item["url"] = product.css('h3 a::attr(href)').get()
            yield product_item

        next_page = response.css('div.pagination a.arrow_pag:last-of-type').attrib.get('href')
        next_pages = response.css('div.pagination a.inactive::attr(href)').getall()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            for next_page2 in next_pages:
                yield response.follow(next_page2, callback=self.parse)

