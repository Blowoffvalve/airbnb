import os
import time
import yaml
from selenium import webdriver
from selenium.common import exceptions
import json

# Load config
#__file__ = os.path.abspath(os.curdir) + "\\src\\findListing.py"
configDir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, 'config'))
outputDir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, 'output'))
selectors = yaml.safe_load(open(configDir + "\\selectors.yaml", "r"))
config = yaml.safe_load(open(configDir + "\\config.yaml", "r"))
outputFile = outputDir + "\\listings.json"

driver = webdriver.Chrome()
url = "http://www.airbnb.com"
driver.get(url)

# Change to listener for network activity
time.sleep(config['listingLoadDelay'])

def submitSearchTerms(driver):
    searchEntryWindow = driver.find_element_by_css_selector(selectors["searchEntrySelector"])
    locationSearchBox = searchEntryWindow.find_element_by_css_selector(selectors["locationSearchSelector"])

    # input the location you're interested in.
    searchParam = " ".join([config["destination"], config["destinationUniquifier"], config["houseListingSuffix"]])
    locationSearchBox.send_keys(searchParam)
    locationSearchBox.submit()


def getListingsOnPage(driver):
    pageListings = list()
    listingElements = driver.find_elements_by_css_selector(selectors["searchListingSelector"])
    for listingElem in listingElements:
        listing = {}
        element = listingElem.find_element_by_css_selector(selectors["searchListingURLSelector"])
        listing["URL"] = element.get_attribute("href").split("?")[0]
        listing["id"] = element.get_attribute("href").split("/")[4].split("?")[0]

        try:    # New listings don't have this
            # get listing rating
            listing["rating"] = float(listingElem.find_element_by_css_selector(selectors["listingRatingSelector"]).text)
            # Get review count
            reviewCount = listingElem.find_element_by_css_selector(selectors["listingReviewCountSelector"]).text
            listing["reviewCount"] = int(reviewCount[1:-1])
        except exceptions.NoSuchElementException:   # If new listing, set rating and review count to -1
            listing["rating"] = -1
            listing["reviewCount"] = -1

        # Get pricing details
        element = listingElem.find_element_by_css_selector("._61b3pa")
        pricingElement = element.find_element_by_css_selector(selectors["listingPriceSelector"])
        listing["price"] = pricingElement.find_element_by_xpath("..").text.split()[1]
        pageListings.append(listing)
    return pageListings


def getListingsNextPage(driver):
    element = driver.find_elements_by_css_selector(selectors['nextPageSelector'])[-1]
    # Check if an svg exists inside the next review page button. If it doesn't, then you're on the last page.
    try:
        element.find_element_by_css_selector("svg")
        coordinates = element.location  # returns dict of X, Y coordinates
        #print(element.location_once_scrolled_into_view)
        #print(element.location)
        coordinates['y'] -= 100
        driver.execute_script("window.scrollTo({}, {})".format(coordinates["x"], coordinates["y"]))
        element.click()
        return 1
    except exceptions.NoSuchElementException:
        return 0


def getAllListings(driver):
    listings = []
    time.sleep(config['listingLoadDelay'])
    while getListingsNextPage(driver) and len(listings)<=int(config["numListingsFromSearch"]):
        time.sleep(config['listingLoadDelay'])
        listings.extend(getListingsOnPage(driver))
    return listings


submitSearchTerms(driver)
listings = getAllListings(driver)
driver.close()

with open(outputFile, "w") as fileHandle:
    json.dump(listings, fileHandle)