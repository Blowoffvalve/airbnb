import requests
from bs4 import BeautifulSoup
import json
import extractListingDetails

page = requests.get("https://www.airbnb.com/rooms/16331385")
soup = BeautifulSoup(page.content, 'html.parser')
#b = json.loads(str(soup.find_all(type = "application/json")[0]).split("<!--")[1].split("-->")[0])
listing = json.loads(str(soup.find_all(type = "application/json")[0]).split("<!--")[1].split("-->")[0])["bootstrapData"]["reduxData"]["homePDP"]["listingInfo"]["listing"]

extractor = extractListingDetails()

import extractListingDetails
extractor.get_photos(listing) 
extractor.get_room_bed_details(listing) 
