import os
import time
import yaml
from selenium import webdriver
from selenium.common import exceptions
import json
import logging
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Load config
#__file__ = os.path.abspath(os.curdir) + "\\src\\getListing.py"
outputDir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, 'output'))
configDir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, 'config'))
selectors = yaml.safe_load(open(configDir + "\\selectors.yaml", "r"))
config = yaml.safe_load(open(configDir + "\\config.yaml", "r"))
inputFile = "\\".join([outputDir, config["listingsFile"]])
outputFile = "\\".join([outputDir, config["populatedListingsFile"]])

driver = webdriver.Chrome()

populatedListings = []
#listing = {}
#listingID = 13650069
#listingURL = "http://www.airbnb.com/rooms/"+str(listingID)
#driver.get(listingURL)

# Change to listener for network activity
#time.sleep(config['listingLoadDelay'])


def expandAllReviews(driver):
    """
    This takes a web page and clicks 'Read More' on the reviews
    :param driver: webdriver instance
    """
    readMoreReviewsSelector = " ".join(["#reviews ", selectors["readMoreSelector"]])
    for element in driver.find_elements_by_css_selector(readMoreReviewsSelector):
        coordinates = element.location  # returns dict of X, Y coordinates
        coordinates['y']-=100
        driver.execute_script("window.scrollTo({}, {})".format(coordinates["x"], coordinates["y"]))
        try:
            element.click()
        except Exception as e:
            #print(e)
            pass


def getReviewsNextPage(driver):
    """
    Go to the next page if one exists else return 0.
    :param driver: webdriver instance
    :return: 1 if there is a new page and 0 otherwise
    """
    reviewsNextPageSelector = " ".join(["#reviews", selectors['nextPageSelector']])
    element = driver.find_element_by_css_selector(reviewsNextPageSelector)
    # Check if an svg exists inside the next review page button. If it doesn't, then you're on the last page.
    try:
        element.find_element_by_css_selector("svg")
        coordinates = element.location  # returns dict of X, Y coordinates
        #print(element.location_once_scrolled_into_view)
        #print(element.location)
        coordinates['y'] -= 200
        driver.execute_script("window.scrollTo({}, {})".format(coordinates["x"], coordinates["y"]))
        element.click()
        return 1
    except exceptions.NoSuchElementException:
        return 0


def translateReviews(driver):
    """
    Check if the reviews contains a foreign language review. If yes, translate the review. This should only be called
    once per listing.
    :param driver: webdriver instance
    :return: 1 if review translation has been done, else 0
    """
    try:
        element = driver.find_element_by_css_selector(selectors['translateReviewsSelector'])
        coordinates = element.location
        coordinates['y'] -= 100
        driver.execute_script("window.scrollTo({}, {})".format(coordinates["x"], coordinates["y"]))
        element.click()
        time.sleep(config['googleTranslateDelay'])  # Wait 2 seconds for the response from google translate
        return 1
    except exceptions.NoSuchElementException:
        return 0


def getReviewsFromPage(driver):
    """
    Get all the reviews on a single page
    :param driver:webdriver instance
    :return: List of reviews on the page without any cleaning applied
    """
    reviews = []
    reviewTextSelector = selectors['reviewTag'] + " " + selectors['textSelector']
    elements = driver.find_elements_by_css_selector(reviewTextSelector)
    for element in elements: # The first 6 elements the selector gets are the
        # print(len(reviews))
        # To remove replies, check if the parent of the review is already in the list(meaning this text is a host's
        # response). If so, don't retrieve it.
        reviewParent = element.find_element_by_xpath("../../../../..")
        reviewParentText = reviewParent.find_element_by_css_selector(reviewTextSelector).text
        reviewText = element.text
        if (len(reviewText) < 13 and reviewText in ["Cleanliness", "Communication", "Check-in", "Accuracy",
                                                    "Location", "Value"]) or ord(reviewText[0]) == 8230:
            continue
        reviewText.encode('utf8')
        if len(reviews) == 0:
            reviews.append(reviewText)
        else:
            if (reviewParentText != reviews[-1]) or config['retrieveHostResponse']:
                reviews.append(reviewText)
        #print(reviewText)
    #print(len(reviews))
    #print(reviews)
    return reviews


def getAllListingReviews(driver):
    """
    Get all the listings from a listing across all its pages in webDriver's Language
    :param driver: webdriver instance
    :return: List of reviews for a listing
    """
    time.sleep(config['listingLoadDelay'])
    translated = translateReviews(driver)# Translate reviews if a translate button exists on the first page
    reviews = getReviewsFromPage(driver)
    while len(reviews)<=config["maxReviewsPerListing"] and getReviewsNextPage(driver) :
        # print(len(reviews))
        time.sleep(config['listingLoadDelay'])
        if translated==0:
            translated = translateReviews(driver)
        expandAllReviews(driver)
        reviews.extend(getReviewsFromPage(driver))
        # print(translated)
    return reviews[:config["maxReviewsPerListing"]]


def getListingCapacity(driver):
    elements = driver.find_elements_by_css_selector(selectors["listingDetailsSelector"])
    listingCapacity = elements[0].text.split("\n")  #This returns a \n separated list of the capacity of the listing
    listing['guestCount'] = int(listingCapacity[-4].split(" ")[0])
    try:
        listing["bedroomCount"] = int(listingCapacity[-3].split(" ")[0])
    except ValueError:
        listing["bedroomCount"] = listingCapacity[-3]
    listing["bedCount"] = int(listingCapacity[-2].split(" ")[0])
    listing["bathRoomCount"] = int(listingCapacity[-1].split(" ")[0])


def getListingAmenities(driver):
    # Click the show all amenities button
    element = driver.find_element_by_css_selector(selectors["amenitiesSelector"])
    coordinates = element.location
    coordinates['y'] -= 100
    driver.execute_script("window.scrollTo({}, {})".format(coordinates["x"], coordinates["y"]))
    element.find_element_by_css_selector(selectors["readMoreSelector"]).click()  # Show all amenitites of this listing
    time.sleep(config['listingLoadDelay'])

    # Navigate the popup
    amenitiesPopup = driver.find_element_by_css_selector(selectors["amenitiesPopUpSelector"])
    amenitiesSection1stLevel = amenitiesPopup.find_element_by_tag_name("section")
    amenitiesSections = amenitiesSection1stLevel.find_elements_by_tag_name("section")

    # Get all amenities and the section they fall under
    sections = {}
    for section in amenitiesSections:
        sectionName = section.find_element_by_css_selector(selectors["amenitySectionNameSelector"]).text
        if sectionName != "Not included":
            sectionElements = section.find_elements_by_css_selector(selectors["textSelector"])
            sectionAmenitiesList = []
            for element in sectionElements:
                sectionAmenitiesList.append(element.text)
            sections[sectionName] = sectionAmenitiesList
        else:
            sectionElements = section.find_elements_by_css_selector(selectors["unavailableAmenitySelector"])
            sectionAmenitiesList = []
            for element in sectionElements:
                sectionAmenitiesList.append(element.text)
            sections[sectionName] = sectionAmenitiesList
    listing["amenities"] = sections


with open(inputFile, "r") as fileHandle:
    listings = json.load(fileHandle)

for item in listings:
    try:
        # Change to listener for network activity
        time.sleep(config['listingLoadDelay'])
        listing = dict()
        listing["id"] = item["id"]
        driver.get(item["URL"])
        listing["reviews"] = getAllListingReviews(driver)
        getListingCapacity(driver)
        getListingAmenities(driver)
        populatedListings.append(listing)
    except:
        print("Problem processing listing {}".format(item["id"]))

with open(outputFile, "w") as fileHandle:
    json.dump(populatedListings, fileHandle)

driver.close()