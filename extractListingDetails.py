class ExtractListingDetails:
    """I am not using static methods because i intend to use an __init__ to get all this details into one dictionary that i'll write to a file"""
    properties = {}
    
    def __init__(self, listing, image_size = "small"):
        self.listing = listing
        self.photo_size = image_size
        self.get_additional_rules()
        self.get_bathroom_label()
        self.get_bed_details()
        self.get_bed_label()
        self.get_bedroom_label()
        self.get_checkin_accuracy_rating()
        self.get_checkin_time_localized()
        self.get_checkout_time_localized()
        self.get_children_allowed()
        self.get_city_localized()
        self.get_cleanliness_rating()
        self.get_communication_rating()
        self.get_country_code()
        self.get_events_allowed()
        self.get_guest_capacity()
        self.get_guest_controls()
        self.get_has_essentials()
        self.get_highlights()
        self.get_home_tier()
        self.get_host_details()
        self.get_host_id()
        self.get_host_is_superhost()
        self.get_host_join_date()
        self.get_host_languages()
        self.get_host_response_rate()
        self.get_host_response_time()
        self.get_host_verified()
        self.get_infants_allowed()
        self.get_instantBook_possible()
        self.get_is_hotel()
        self.get_latitude()
        self.get_listing_accuracy_rating()
        self.get_listing_expectations()
        self.get_listing_page()
        self.get_listing_requires_license()
        self.get_listing_tier()
        self.get_listing_type()
        self.get_location()
        self.get_location_rating()
        self.get_longitude()
        self.get_native_currency()
        self.get_no_reviews()
        self.get_overall_guest_satisfaction()
        self.get_pets_allowed()
        self.get_photos_urls()
        self.get_property_type()
        self.get_rating()
        self.get_room_bed_details()
        self.get_smoking_allowed()
        self.get_value_rating()
        self.get_visible_review_count()
        
        
    def get_no_reviews(self):
        """I get the number of reviews from the visible review count atttribute. Not sure if this is total review count for the listing or just the visible ones because Airbnb selects what reviews are shown to guests"""
        """Verified this by checking content of listing["review_details_interface"]["review_count"]. The number is correct."""
        return self.listing["visible_review_count"]
    
    def get_rating(self):
        return self.listing["star_rating"]
    
    def get_additional_rules(self):
        """Get the additional rules of the listing for NLP analysis later(maybe)"""
        self.properties["additional_rules"] = self.listing["additional_house_rules"]
    
    def get_bathroom_label(self):
        """Get the number and types of bathrooms in listing"""
        self.properties["bathroom_label"] = self.listing["bathroom_label"]
    
    def get_bed_label(self):
        self.properties["bed_count"] =  self.listing["bed_label"]
    
    def get_bedroom_label(self):
        """This returns the type of bedroom(s) a listing has. Values include *2 bedrooms*, *studio*
        """
        self.properties["bedroom_type"] =  self.listing["bedroom_label"]
    
    def get_country_code(self):
        """Returns the 2 character country code for the country according to ISO 3166-1 alpha-2 codes. Reference https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2"""
        self.properties["country_code_2"] = self.listing["country_code"]
      
    def get_guest_controls(self):
        """ This has a bunch of details in it and will be called to retrieve those details"""
        return self.listing["guest_controls"]
    
    def get_children_allowed(self):
        self.properties["children_allowed"] = self.get_guest_controls()["allows_children"]
    
    def get_events_allowed(self):
        self.properties["events_allowed"] = self.get_guest_controls()["allows_events"]
    
    def get_infants_allowed(self):
        self.properties["infants_allowed"] = self.get_guest_controls()["allows_infants"]
    
    def get_pets_allowed(self):
        self.properties["pets_allowed"] = self.get_guest_controls()["allows_pets"]
    
    def get_smoking_allowed(self):
        self.properties["smoking_allowed"] = self.get_guest_controls()["allows_smoking"]
    
    def get_guest_capacity(self):
        """This contains the number of guests in the listing"""
        """
        return listing["guest_label"]
        """
        self.properties["guest_capacity"] = self.get_listing_logs()["person_capacity"]
    
    def get_has_essentials(self):
        self.properties["has_essential_amenities"] =self.listing["has_essentials_amenity"]
    
    def get_highlights(self):
        highlights = []
        for items in self.listing["highlights"]:
            highlights.append(items["headline"])
        self.properties["highlights"] = highlights
    
    def get_bed_details(self):
        """Get the number of beds of each type in the listing. 
        This data is in multiple locations"""
        """
        beds = []
        for items in listing["hometour_rooms"]:
            for bed in items["highlights_hometour"]:
                beds.append(bed)
        """
        beds = {}
        listing_rooms = self.get_room_bed_details()
        for room in listing_rooms:
            room = listing_rooms[room]
            for bed in room:
                if(beds.get(bed)):
                    beds[bed] = beds[bed] + room[bed]
                else:
                    beds[bed] = room[bed]
        self.properties["bed_type_counts"] =  beds
    
    def get_room_bed_details(self):
        """Get the number of rooms and the beds in them"""
        rooms = {}
        for room in self.listing["listing_rooms"]:
            beds = {}
            for bed in room["beds"]:
                beds[bed["type"]] = bed["quantity"]
            rooms[room["room_number"]] = beds
        self.properties["room_bed_distribution"] = rooms
        return rooms
    
    def get_is_hotel(self):
        self.properties["is_hotel"] = self.listing["is_hotel"]
    
    def get_latitude(self):
        """
        return listing["lat"]
        """
        self.properties["location_latitude"] = self.get_listing_logs()["listing_lat"]
    
    def get_longitude(self):
        """
        return listing["lng"]
        """
        self.properties["location_longitude"] = self.get_listing_logs()["listing_lng"]
    
    def get_checkin_time_localized(self):
        """This returns the earliest check in time in the listing's local time"""
        ###I return the 2nd value since the values in this field are usually in the format
        ###*After XXPM* 
        self.properties["checkin_local_time"] =  self.listing["localized_check_in_time_window"].split(" ")[1]
    
    def get_checkout_time_localized(self):
        """This returns the check out time in the listing's local time"""
        self.properties["checkout_local_time"] =  self.listing["localized_check_out_time"]
    
    def get_city_localized(self):
        """This returns the name of the city in the local language e.g. Bombay vs Mumbai"""
        self.properties["city_local_name"] = self.listing["localized_city"]

    def get_location(self):
        self.properties["location"] = self.listing["location_title"]
        
    def get_listing_expectations(self):
        """This returns unique expectations for the listing e.g. Security deposit requirements, presence of staircase"""
        le = {}
        expectations = self.listing["localized_listing_expectations"]
        for expectation in expectations:
            le[expectation["type"]] = expectation["title"]
        self.properties["listing_expectations"] = le
    
    def get_listing_type(self):
        """This returns the type of the listing including whether the listing is a whole apartment or just a room in an apartment"""
        """
        return listing["localized_room_type"]
        """
        self.properties["listing_type"] = self.get_listing_logs()["room_type"]
    
    def get_native_currency(self):
        """This doesn't seem to match the currency of the country. I am assuming it refers to the currency you'll be billed in"""
        self.properties["native_currency"] = self.listing["native_currency"]
    
    def get_listing_logs(self):
        """I get info from p3_event_data_logging and use this to create a number of other methods"""
        return self.listing["p3_event_data_logging"]
    
    def get_listing_accuracy_rating(self):
        self.properties["rating_listing_accuracy"] = self.get_listing_logs()["accuracy_rating"]
    
    def get_checkin_accuracy_rating(self):
        self.properties["rating_checkin_accuracy"] =  self.get_listing_logs()["checkin_rating"]
    
    def get_cleanliness_rating(self):
        self.properties["rating_cleanliness"] = self.get_listing_logs()["cleanliness_rating"]
    
    def get_communication_rating(self):
        self.properties["rating_communication"] =  self.get_listing_logs()["communication_rating"]
    
    def get_overall_guest_satisfaction(self):
        self.properties["rating_guest_satisfaction"] = self.get_listing_logs()["guest_satisfaction_overall"]
    
    def get_home_tier(self):
        self.properties["home_tier"] = self.get_listing_logs()["home_tier"]
    
    def get_host_is_superhost(self):
        """ Get superhost status of listing host"""
        """ return self.get_listing_logs(listing)["is_superhost"] """
        self.properties["super_host"] = self.get_host_details()["is_superhost"]
    
    def get_instantBook_possible(self):
        self.properties["instant_book_allowed"] = self.get_listing_logs()["instant_book_possible"]
    
    def get_location_rating(self):
        self.properties["location_rating"] = self.get_listing_logs()["location_rating"]
    
    def get_listing_page(self):
        self.properties["listing_page"] = self.get_listing_logs()["page"]
    
    def get_value_rating(self):
        self.properties["value_ranking"] = self.get_listing_logs()["value_rating"]
    
    def get_visible_review_count(self):
        self.properties["visible_review_count"] = self.get_listing_logs()["visible_review_count"]
    
    def get_photos_urls(self):
        """Several photo sizes are available including large, large_cover, medium, mini, small, x_large, x_large_cover, x_medium, x_small, xl_picture, xx_large. Retuns a dictionary of dictionaries"""
        photos = {}
        listing_photos= self.listing["photos"]
        for photo in listing_photos:
            photos[photo["id"]]= photo[self.photo_size]
        self.properties["photos_urls"] = photos
    
    def get_host_details(self):
        return self.listing["primary_host"]
    
    def get_host_id(self):
        self.properties["host_id"] = self.get_host_details()["id"]
    
    def get_host_verified(self):
        self.properties["host_verified"] = self.get_host_details()["identity_verified"]
    
    def get_host_languages(self):
        self.properties["host_languages"] = self.get_host_details()["languages"]
    
    def get_host_join_date(self):
        self.properties["host_join_date"] = self.get_host_details()["member_since"]
    
    def get_host_response_rate(self):
        self.properties["host_response_rate"] = self.get_host_details()["response_rate_without_na"]
    
    def get_host_response_time(self):
        self.properties["host_average_response_delay"] = self.get_host_details()["response_time_without_na"]
    
    def get_listing_requires_license(self):
        self.properties["listing_requires_license"] = self.listing["requires_license"]
    
    def get_property_type(self):
        """This shows the property type. Important because it shows you if you have only the apartment to your self or the whole home(including a garden and other amenities that are part of the house)"""
        self.properties["property_type"] = self.listing["room_and_property_type"]
    
    def get_listing_tier(self):
        self.properties["listing_tier"] = self.listing["tier_id"]