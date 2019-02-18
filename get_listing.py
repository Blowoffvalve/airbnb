import requests
from bs4 import BeautifulSoup
import json
from extractListingDetails import ExtractListingDetails

page = requests.get("https://www.airbnb.com/rooms/14454178")
soup = BeautifulSoup(page.content, 'html.parser')
#b = json.loads(str(soup.find_all(type = "application/json")[0]).split("<!--")[1].split("-->")[0])
response = json.loads(str(soup.find_all(type = "application/json")[0]).split("<!--")[1].split("-->")[0])["bootstrapData"]["reduxData"]["homePDP"]["listingInfo"]["listing"]


listing = ExtractListingDetails(response)
listing.properties