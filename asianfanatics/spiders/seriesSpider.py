import scrapy


class SeriesspiderSpider(scrapy.Spider):
    name = "seriesSpider"
    allowed_domains = ["asyafanatiklerim.com"]
    start_urls = ["https://asyafanatiklerim.com/dizi/the-three-musketeers/"]

    def parse(self, response):

        content = response.css("div.content")
        #episode_list = content.css("ul.episodios li")
        cast_div =  content.css("div#cast div.persons")
        persons = cast_div.css("div.persons div.person")

        cast_list= []
        for person in persons:
            actor_dict = {
                "name": person.css("div.data div.name a::text").get(),
                "caracter": person.css("div.data div.caracter::text").get() 
            }

            cast_list.append(actor_dict)
        yield{
            "name": content.css("div.data h1::text").get(),
            "full_date": content.css("span.date::text").get(),
            "total_episode": content.css('div.custom_fields b.variante:contains("Bölümler") + span.valor::text').get(),
            "cast": cast_list
        }

