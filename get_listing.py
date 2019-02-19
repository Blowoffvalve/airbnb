import requests
from bs4 import BeautifulSoup
import json
from extractListingDetails import Listing

page = requests.get("https://www.airbnb.com/rooms/12964428")
#12964428
#22475432
#16331385
#16038702
#427077
#9472023
soup = BeautifulSoup(page.content, 'html.parser')
#b = json.loads(str(soup.find_all(type = "application/json")[0]).split("<!--")[1].split("-->")[0])
response = json.loads(str(soup.find_all(type = "application/json")[0]).split("<!--")[1].split("-->")[0])

#json.dump(response,open("response.txt", "w"))
listing = Listing(response)
listing.properties