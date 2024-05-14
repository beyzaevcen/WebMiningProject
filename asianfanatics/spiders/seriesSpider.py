import scrapy
import pandas as pd
import time
import random

class SeriesspiderSpider(scrapy.Spider):
    name = "seriesSpider"
    allowed_domains = ["asyafanatiklerim.com"]
    #start_urls = ["https://asyafanatiklerim.com/dizi/knight-flower/"]

    def start_requests(self):
        df = pd.read_csv("C:\\Users\\fzehr\\OneDrive\\Belgeler\\GitHub\\WebMiningProject\\series_by_year.csv")
        url_list = df["url"].str.strip()

        for url in url_list:
            wait_time = random.uniform(2, 4)
            time.sleep(wait_time)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = response.css("div.content")
        cast_div =  content.css("div#cast div.persons")
        persons = cast_div.css("div.persons div.person")
        categories = content.css("div.sgeneros a::text").getall()
        evulate = content.css("div.user_control span::text").getall()

        cast_list = []
        for person in persons:
            actor_dict = {
                "name": person.css("div.data div.name a::text").get(),
                "caracter": person.css("div.data div.caracter::text").get() 
            }
            cast_list.append(actor_dict)

        cat_list = []
        for category in categories:
            cat_list.append(category)


        like = []
        watch = []
        for index, evul in enumerate(evulate):
            if index == 0:
                like.append(evul)
            elif index == 1:
                watch.append(evul)

        yield {
            "name": content.css("div.data h1::text").get(),
            "total_episode": content.css('div.custom_fields b.variante:contains("Bölümler") + span.valor::text').get(),
            "rating":content.css("div.dt_rating_data div.starstruck-rating span::text").get(),
            "like": like,
            "watch": watch,
            "cast": cast_list,
            "category": cat_list
        }
