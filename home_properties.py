import scrapy

class ListingSpider(scrapy.Spider):
    #Properties of the spider
    name = "ListingSpider"
    start_urls = ["https://www.airbnb.com/rooms/427077"]
    
    #File handle to write the properties of a file to a CSV file
    #f = open("apartment.csv", "a+")
    
    def get_amenities(self, text):
        #File handle to write the properties of a file to a CSV file
        f = open("apartment.csv", "a+")
        start_index = text.index('"listing_amenities":')
        stop_index = text.index("]", start_index)
        #substring the text to only include relevant data
        text = text[int(start_index): int(stop_index)]
        start_index = 0
        
        #Write the listing_Id to the file
        url = str(self.start_urls)
        f.write(url[url.index("/rooms")+7:-2])
        
        #Loop through the text to get the amenities
        #Get number of appearances of "name" in the text
        name_count = text.count("name")
        for x in range(name_count):
            start_index = text.index("name", start_index)+ 7
            stop_index = text.index('",', start_index)
            f.write("," + text[start_index: stop_index])
        f.write("\n")   
    
    def parse(self, response):
        #Selector to get the script that contains "application/json"
        SCRIPT_SELECTOR = "//script[@type ='application/json']/text()"
        for script in response.xpath(SCRIPT_SELECTOR):
            text = script.extract()
            ## Get the listing_amenities
            if "listing_amenities" in text:
                self.get_amenities(text)
                