# Airbnb prediction
Airbnb listing extractor for varying ML projects

## Requirements
1. Install the following python packages
    - Selenium
    - pyyaml
2. Setup chromedriver as listed [here](http://www.automationtestinghub.com/selenium-chromedriver/). Ensure 
chromedriver is at the root directory of the application folder.

## Instructions

### To get a list of apartment listings in a location
1. Configure the following parameters in the [config file](config/config.yaml)
    - destination: This should contain the name of the location you want to retrieve listings from.
    - destinationUniquifier: This should contain the state/ province/ country information to uniquely identify the 
    location.
    - numListingsFromSearch: The number of listings you want to retrieve from the search API. As of the time i last 
    tested this code, that number is 288.
    - listingsFile: The file in [output](/output) that the listings is written to.
2. Run findListings.py using `python findListings.py`. The listings are written to the file specified in the  
[config file](config/config.yaml) as the `listingsFile` parameter. See  this [example](output/listings.json).

### To retrieve a listing's details from listingsFile
1. Configure the following parameters in the [config file](config/config.yaml)
    - retrieveHostResponse: This accepts 0 `No` or 1 `Yes`, and determines whether to include the host's response in
    the extracted reviews.
    - maxReviewsPerListing: This determines the maximum number of reviews to retrieve from each listing.
    -populatedListingsFile: The file in [output](/output) that the file containing the listings is written to.
2. Run getListings.py using `python getListings.py`. The output is written to the file specified in the [config file]/
(config/config.yaml) as the `populatedListingsFile` parameter. See this [example](output/populatedListings.json).
## Compatibility
I tested this application with python 3.6. YMMV if you use another version, however i expect it to be stable for python
3.X.

## To do
1. Use logging to properly log debug messages instead of printing.
2. Stop using static values for waits and figure out how to establish that all the elements of a page have been loaded.
3. Expand documentation on [selectors](config/selectors.yaml) so it's clear what each selector is doing. Current 
status is too arcane.
4. Add a config that does the scraping using a headless browser.
5. Alter getListings to allow you exclude listings that aren't initially in English