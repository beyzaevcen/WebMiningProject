import scrapy
import pandas as pd
import time
import random

class SeriesspiderSpider(scrapy.Spider):
    name = "seriesSpider"
    allowed_domains = ["asyafanatiklerim.com"]

    def start_requests(self):
        df = pd.read_csv("C:\\Users\\fzehr\\OneDrive\\Belgeler\\GitHub\\WebMiningProject\\asianfanatics\\alldatas.csv")
        url_list = df["url"].str.strip()

        for url in url_list:
            wait_time = random.uniform(3, 7)
            time.sleep(wait_time)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = response.css("div.content")
        cast_div =  content.css("div#cast div.persons")
        persons = cast_div.css("div.persons div.person")

        cast_list = []
        for person in persons:
            actor_dict = {
                "name": person.css("div.data div.name a::text").get(),
                "caracter": person.css("div.data div.caracter::text").get() 
            }
            cast_list.append(actor_dict)
        yield {
            "name": content.css("div.data h1::text").get(),
            "full_date": content.css("span.date::text").get(),
            "total_episode": content.css('div.custom_fields b.variante:contains("Bölümler") + span.valor::text').get(),
            "cast": cast_list
        }
