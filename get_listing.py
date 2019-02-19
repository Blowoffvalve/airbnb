import requests
from bs4 import BeautifulSoup

from extractListingDetails import Listing

def get_listing(listingId):
    listing_url = "https://www.airbnb.com/rooms/" + str(listingId)
    page = requests.get(listing_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    listing = Listing(soup)
    return listing.properties


#12964428
#22475432
#16331385
#16038702
#427077
#9472023
lid = get_listing(9472023)
print(lid["city_name"])
print(lid["state_name"])
print(lid["country_name"])