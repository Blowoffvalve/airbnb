class extractListingDetails:
    """I am not using static methods because i intend to use an __init__ to get all this details into one dictionary that i'll write to a file"""
    def get_no_reviews(self, listing):
        """I get the number of reviews from the visible review count atttribute. Not sure if this is total review count for the listing or just the visible ones because Airbnb selects what reviews are shown to guests"""
        """Verified this by checking content of listing["review_details_interface"]["review_count"]. The number is correct."""
        return listing["visible_review_count"]
    
    def get_rating(self, listing):
        return listing["star_rating"]
    
    def get_additional_rules(self, listing):
        """Get the additional rules of the listing for NLP analysis later(maybe)"""
        return listing["additional_house_rules"]
    
    def get_bathroom_label(self, listing):
        return listing["bathroom_label"]
    
    def get_bed_label(self, listing):
        return listing["bed_label"]
    
    def get_bedroom_label(self, listing):
        return listing["bedroom_label"]
    
    def get_country_code(self, listing):
        return listing["country_code"]
      
    def get_guest_controls(self, listing):
        """ This has a bunch of details in it and will be called to retrieve those details"""
        return listing["guest_controls"]
    
    def get_children_allowed(self, listing):
        return self.get_guest_controls(listing)["allows_children"]
    
    def get_events_allowed(self, listing):
        return self.get_guest_controls(listing)["allows_events"]
    
    def get_infants_allowed(self, listing):
        return self.get_guest_controls(listing)["allows_infants"]
    
    def get_pets_allowed(self, listing):
        return self.get_guest_controls(listing)["allows_pets"]
    
    def get_smoking_allowed(self, listing):
        return self.get_guest_controls(listing)["allows_smoking"]
    
    def get_guest_capacity(self, listing):
        """
        return listing["guest_label"]
        """
        return self.get_listing_logs(listing)["person_capacity"]
    
    def get_has_essentials(self, listing):
        return listing["has_essentials_amenity"]
    
    def get_highlights(self, listing):
        highlights = []
        for items in listing["highlights"]:
            highlights.append(items["headline"])
        return highlights
    
    def get_bed_details(self, listing):
        """Get the number of beds of each type in the listing. This data is in multiple locations"""
        """
        beds = []
        for items in listing["hometour_rooms"]:
            for bed in items["highlights_hometour"]:
                beds.append(bed)
        """
        beds = {}
        listing_rooms = self.get_room_bed_details(listing)
        for room in listing_rooms:
            room = listing_rooms[room]
            for bed in room:
                if(beds.get(bed)):
                    beds[bed] = beds[bed] + room[bed]
                else:
                    beds[bed] = room[bed]
        return beds
    
    def get_room_bed_details(self, listing):
        """Get the number of rooms and the beds in them"""
        rooms = {}
        for room in listing["listing_rooms"]:
            beds = {}
            for bed in room["beds"]:
                beds[bed["type"]] = bed["quantity"]
            rooms[room["room_number"]] = beds
        return rooms
    
    def get_is_hotel(self, listing):
        return listing["is_hotel"]
    
    def get_latitude(self, listing):
        """
        return listing["lat"]
        """
        return self.get_listing_logs(listing)["listing_lat"]
    
    def get_longitude(self, listing):
        """
        return listing["lng"]
        """
        return self.get_listing_logs(listing)["listing_lng"]
    
    def get_checkin_time_localized(self, listing):
        """This returns the check in time in the listing's local time"""
        return listing["localized_check_in_time_window"]
    
    def get_checkout_time_localized(self, listing):
        """This returns the check out time in the listing's local time"""
        return listing["localized_check_out_time"]
    
    def get_city_localized(self, listing):
        """This returns the name of the city in the local language e.g. Bombay vs Mumbai"""
        return listing["localized_city"]

    def get_location(self, listing):
        return listing["location_title"]
        
    def get_listing_expectations(self, listing):
        """This returns unique expectations for the listing e.g. Security deposit requirements, presence of staircase"""
        le = {}
        expectations = listing["localized_listing_expectations"]
        for expectation in expectations:
            le[expectation["type"]] = expectation["title"]
        return le
    
    def get_listing_type(self, listing):
        """This returns the type of the listing including whether the listing is a whole apartment or just a room in an apartment"""
        """
        return listing["localized_room_type"]
        """
        return self.get_listing_logs(listing)["room_type"]
    
    def get_native_currency(self, listing):
        """This doesn't seem to match the currency of the country. I am assuming it refers to the currency you'll be billed in"""
        return listing["native_currency"]
    
    def get_listing_logs(self, listing):
        """I get info from p3_event_data_logging and use this to create a number of other methods"""
        return listing["p3_event_data_logging"]
    
    def get_listing_accuracy_rating(self, listing):
        return self.get_listing_logs(listing)["accuracy_rating"]
    
    def get_checkin_accuracy_rating(self, listing):
        return self.get_listing_logs(listing)["checkin_rating"]
    
    def get_cleanliness_rating(self, listing):
        return self.get_listing_logs(listing)["cleanliness_rating"]
    
    def get_communication_rating(self, listing):
        return self.get_listing_logs(listing)["communication_rating"]
    
    def get_overall_guest_satisfaction(self, listing):
        return self.get_listing_logs(listing)["guest_satisfaction_overall"]["guest_satisfaction_overall"]
    
    def get_home_tier(self, listing):
        return self.get_listing_logs(listing)["home_tier"]
    
    def get_is_superhost(self, listing):
        """ return self.get_listing_logs(listing)["is_superhost"] """
        return self.get_host_details(listing)["is_superhost"]
    
    def get_instantBook_possible(self, listing):
        return self.get_listing_logs(listing)["instant_book_possible"]
    
    def get_location_rating(self, listing):
        return self.get_listing_logs(listing)["location_rating"]
    
    def get_listing_page(self, listing):
        return self.get_listing_logs(listing)["page"]
    
    def get_value_rating(self, listing):
        return self.get_listing_logs(listing)["value_rating"]
    
    def get_visible_review_count(self, listing):
        return self.get_listing_logs(listing)["visible_review_count"]
    
    def get_photos(self, listing, photo_size = "large"):
        """Several photo sizes are available including large, large_cover, medium, mini, small, x_large, x_large_cover, x_medium, x_small, xl_picture, xx_large. Retuns a dictionary of dictionaries"""
        photos = {}
        listing_photos= listing["photos"]
        for photo in listing_photos:
            photos[photo["id"]]= photo[photo_size]
        return photos
    
    def get_host_details(self,listing):
        return listing[primary_host]
    
    def get_host_id(self, listing):
        return self.get_host_details(listing)["id"]
    
    def get_host_verified(self, listing):
        return self.get_host_details(listing)["identity_verified"]
    
    def get_host_languages(self, listing):
        return self.get_host_details(listing)["languages"]
    
    def get_host_join_date(self, listing):
        return self.get_host_details(listing)["member_since"]
    
    def get_host_response_rate(self, listing):
        return self.get_host_details(listing)["response_rate_without_na"]
    
    def get_host_response_time(self, listing):
        return self.get_host_details(listing)["response_time_without_na"]
    
    def get_listing_requires_license(self, listing):
        return listing["requires_license"]
    
    def get_property_type(self, listing):
        """This shows the property type. Important because it shows you if you have only the apartment to your self or the whole home(including a garden and other amenities that are part of the house)"""
        return listing["room_and_property_type"]
    
    def get_listing_tier(self, listing):
        return listing("tier")
    