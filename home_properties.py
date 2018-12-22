import scrapy

class ListingSpider(scrapy.Spider):
    name = "ListingSpider"
    start_urls = ["https://www.airbnb.com/rooms/427077"]
    f = open("apartment.csv", "w")
    def parse(self, response):
        SCRIPT_SELECTOR = "//script[@type ='application/json']/text()"
        for script in response.xpath(SCRIPT_SELECTOR):
            text = script.extract()
            if "listing_amenities" in text:
                start_index = text.index('"listing_amenities":')
                stop_index = text.index("]", start_index)
                text = text[int(start_index): int(stop_index)]
                start_index = 0
                name_count = text.count("name")
                for x in range(name_count):
                    start_index = text.index("name", start_index)+ 7
                    stop_index = text.index('",', start_index)
                    print(text[start_index: stop_index])
                    
                    