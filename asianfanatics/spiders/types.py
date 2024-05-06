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

