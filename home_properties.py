import scrapy

class ListingSpider(scrapy.Spider):
    #Properties of the spider
    name = "ListingSpider"
    start_urls = ["https://www.airbnb.com/rooms/427077"]
    f= open("apartment.csv", "a+")
    f.write("Listing_id, No_Of_Reviews, Listing_rating, No_Of_Photos, *Amenities \n")
    #File handle to write the properties of a file to a CSV file
    #f = open("apartment.csv", "a+")
    
    """Method to get the amenities of a listing"""
    def get_amenities(self, text):
        #File handle to write the properties of a file to a CSV file
        start_index = text.index('"listing_amenities":')
        stop_index = text.index("]", start_index)
        #substring the text to only include relevant data
        text = text[int(start_index): int(stop_index)]
        start_index = 0
        
        #Loop through the text to get the amenities
        #Get number of appearances of "name" in the text
        name_count = text.count("name")
        for x in range(name_count):
            start_index = text.index("name", start_index)+ 7
            stop_index = text.index('",', start_index)
            #The amenity Pack ’n Play/travel crib isn't formatted properly
            #in the csv file. The replace let's me change ’n to and
            self.f.write(", " + text[start_index: stop_index].replace("’n", "and"))
        self.f.write("\n")   
    
    """Method to get the Number of reviews and aggregate rating for 
    a listing""" 
    def get_reviews(self, text):
        # Tag "_1dl27thl"> is the closest tag to the number of reviews a 
        #   listing has
        start_index = text.index('"_1dl27thl">')+12
        stop_index = text.index(" ", start_index)
        self.f.write(", " + text[start_index: stop_index])
        #Tag content=" is the closest tag to the aggregate rating for a listing
        start_index = text.index('content="')+9
        self.f.write(", " + text[start_index:start_index+1])
    
    """Method to get the number of photos for a listing"""    
    def get_num_of_photos(self, text):
        #The "thumbnail":"https: is commensurate with the number of
        #photos a listing has
        self.f.write(", " + str(text.count('"thumbnail":"https:')))
        
    def parse(self, response):
        #f = open("apartment.csv", "a+")
        #Write the listing_Id to the file
        url = str(self.start_urls)
        self.f.write(url[url.index("/rooms")+7:-2])
        #Selector to get the script that contains "application/json"
        GENERAL_SELECTOR = "//script[@type ='application/json']/text()"
        RATING_SELECTOR = '//div[@id="reviews"]'
        
        #Get the reviews of the listing
        self.get_reviews(str(response.xpath(RATING_SELECTOR).extract()))
        
        #Get the number of photos
        self.get_num_of_photos(str(response.xpath(GENERAL_SELECTOR).extract()))
        
        #Get the amenities of the listing
        for script in response.xpath(GENERAL_SELECTOR):
            text = script.extract()
            ## Get the listing_amenities
            if "listing_amenities" in text:
                self.get_amenities(text)
        
        