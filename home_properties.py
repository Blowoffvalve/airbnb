import scrapy

class ListingSpider(scrapy.Spider):
    #Properties of the spider
    name = "ListingSpider"
    #I'll make this a generator.
    start_urls = ["https://www.airbnb.com/rooms/"+ str(x) for x in range(16331907, 16331908)]
    #apts = ["16331385","427077"]
    
    custom_setting = {"DOWNLOAD_DELAY":10,
                      "CONCURRENT_REQUESTS_PER_DOMAIN":3
            }
    #File handle to write the properties of a file to a CSV file
    #f = open("apartment.csv", "a+")
    f= open("apartment.csv", "a+")
    f.write("Listing_id, No_Of_Reviews, Listing_rating, location_state,\
            location_country, max_guest_count, bed_count, listing_type, self_checkIn_available,\
            languages, response_rate, response_delay, verified, no_reviews,\
            join_date, checkIn_type, self_checkIn_available, checkIn_time,\
            checkOut_time, checkIn_type, pet_acceptance, beds_type,\
            No_Of_Photos, *Amenities \n")
    
    """Method to get the amenities of a listing. It returns a list
    containing all the amenities in the listing"""
    def get_amenities(self, text):
        retval = []
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
            retval.append(text[start_index: stop_index].replace("’n", "and"))
        return retval   
    
    """Method to get the Number of reviews and aggregate rating for 
    a listing. Returns([NoOfReviews, aggregate rating])""" 
    def get_reviews(self, text):
        # Tag "_1dl27thl"> is the closest tag to the number of reviews a 
        #   listing has
        retval = []
        start_index = text.index('"_1dl27thl">')+12
        stop_index = text.index(" ", start_index)
        retval.append(str(text[start_index: stop_index]))
        #Tag content=" is the closest tag to the aggregate rating for a listing
        start_index = text.index('content="')+9
        stop_index = text.index('"', start_index)
        retval.append(str(text[start_index:stop_index]))
        return retval
    
    """Method to get the number of photos for a listing. Returns the number 
    of photos"""    
    def get_num_of_photos(self, text):
        #The "thumbnail":"https: is commensurate with the number of
        #photos a listing has
        return str(text.count('"thumbnail":"https:'))
    
    
    """Method to get details of the listing. If the response has been garbled,
    the first character returned is 18 *[-1]
    returns([location, guest_count, bed_count, listing_type, self_checkIn_available,
                       languages, response_rate, response_delay, verified, no_reviews, 
                       join_date, checkIn_type, self_checkIn_available, checkIn_time,
                       checkOut_time, checkIn_type, pet_acceptance, beds_type])
    """     
    def get_additional_details(self, text):
        max_guest_count = text[2].split(" ")[0]
        bed_count = text[4].split(" ")[0]
        ret_val = []
        #Airbnb sometimes changes the order of the response("I can't imagine why :)")
        #I set the first value to be returned to -1 so the URL can be called again.
        try:
            max_guest_count = int(max_guest_count)
            bed_count = int(bed_count)
        except:
            return [-1] * 18
            
        listing_type = text[3]
        location = []
        response_rate, join_date, response_delay, languages = "", "", "", ""
        verified, checkIn_time, checkOut_time, checkIn_type = "","", "", ""
        pet_acceptance, beds_type= "",""
        self_checkIn_available,no_reviews = 0,0        
        for loc, item in enumerate(text):
            str_item = str(item)
            if "Languages:" == item:
                languages = ""
                for items in text[loc+2]:
                    languages += str(items).replace(",", "-")
            if "Response rate:" == item:
                response_rate = text[loc+2]
            if "Response time:" == item:
                response_delay = text[loc+2]
            if "\U000f0019" ==item:
                verified = text[loc+1]
            if "\U000f0004" == item:
                no_reviews = text[loc+1].split(" ")[0]
                join_date = str(text[loc-1].split(" ")[-2:-1][0])
                join_date+=" " + str(text[loc-1].split(" ")[-1:][0])
                location = str(text[loc-3])
            if "Check yourself in with the" in str_item:
                checkIn_type = item.split(" ")[-1]
                self_checkIn_available = 1
            if "Check-in is anytime" in str_item:
                checkIn_time = item.split(" ")[4]
                checkOut_time = item.split(" ")[-1]
                pet_acceptance = text[loc-2]
                beds_type = text[loc-3]
        print(text)        
        """print("location:", location, 
              "guest count:", guest_count,
              "Listing type:", listing_type,
              #"bed types",bed_count,
              "Self checkIn available:", self_checkIn_available,
              "Host languages:", languages,
              "response_rate:", response_rate, 
              "Response_delay:", response_delay,
              "Verified:", verified,
              "Number of reviews:", no_reviews,
              "join_date:", join_date,
              "checkIn_type:", checkIn_type,
              "self_checkIn_available:", self_checkIn_available,
              "checkIn_time:", checkIn_time,
              "checkOut_time:", checkOut_time,
              "checkIn_type:", checkIn_type,
              "pet_acceptance:", pet_acceptance,
              "beds_type:", beds_type)"""
        ret_val.extend([location, max_guest_count, bed_count, listing_type, self_checkIn_available,
                       languages, response_rate, response_delay, verified, no_reviews, 
                       join_date, checkIn_type, self_checkIn_available, checkIn_time,
                       checkOut_time, checkIn_type, pet_acceptance, beds_type])
        return ret_val
    
    def parse(self, response):
        try:
            #Selector to get the script that contains "application/json"
            GENERAL_SELECTOR = "//script[@type ='application/json']/text()"
            RATING_SELECTOR = '//div[@id="reviews"]'
            general_data = response.xpath(GENERAL_SELECTOR).extract()
            retval = []
            #Get the reviews of the listing. If Airbnb's server doesn't return
            #valid data, call the URL again
            listing_id = response.css("::attr(href)").extract()[6].split("/")[-1]
            #retval.append(listing_id)
            try:
                review_data = self.get_reviews(str(response.xpath(RATING_SELECTOR).extract()))
            except ValueError:
                scrapy.Request(response.urljoin(self.start_urls[0]),callback = self.parse)
            retval.extend(review_data)
            
            #Get additional_details of the listing
            additional_details = self.get_additional_details(response.css("._1r804a6o").css("::text").extract())
            retval.extend(additional_details)
            if(additional_details[0]=="-1"):
                scrapy.Request(response.urljoin(self.start_urls[0]),callback = self.parse)
            #Get the number of photos
            photo_count = self.get_num_of_photos(str(general_data))
            retval.append(photo_count)
            #Get the amenities of the listing
            for script in general_data:
                ## Get the listing_amenities
                if "listing_amenities" in script:
                    amenities = self.get_amenities(script)
            retval.extend(amenities)
            #Write the listing_Id to the file
            self.f.write(listing_id)
            for i in retval:
                self.f.write(",%s"%i)
            self.f.write("\n")
        except:
            pass
        