# found out how to not display web browser when using selenium here:
# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# TODO: Look at pp. 258 - 275 for further information regarding Flask-based web apps
from flask import Flask, render_template

driver = webdriver.PhantomJS()  # Creates an invisible browser
driver.get('https://google.com/') # Navigates to Google.com
inputString = "applesauce"

searchBarInput = driver.find_element_by_name('q') # Assigns variable to Google Search bar
if inputString != '':
    searchBarInput.send_keys(inputString) # what you are searching for
    searchBarInput.send_keys(Keys.RETURN) # Hit <RETURN> so Google begins searching
    time.sleep(3) # sleep for a bit so the results webpage will be rendered

    # TODO: scrape first two websites that are in the top 10 news websites
    #       according to http://blog.feedspot.com/usa_news_websites/ 's metrics
    urls = driver.find_elements_by_css_selector('h3.r a')
    count = 0
    for url in urls:
        # TODO: scrape according to each website's layout and then run ML algorithm
        # TODO: check if one website is liberal and the other is conservative,
        #       if not scape the next website until requirements are met (probably use flags)
        print(url.get_attribute('href')[29:] + "\n\n")
        if "cnn.com" in url.get_attribute('href')[29:]: # 1
            pass
        if "nytimes.com" in url.get_attribute('href')[29:]: # 2
            pass
        if "huffingtonpost.com" in url.get_attribute('href')[29:]: # 3
            pass
        if "foxnews.com" in url.get_attribute('href')[29:]: # 4
            pass
        if "usatoday.com" in url.get_attribute('href')[29:]: # 5
            pass
        if "reuters.com" in url.get_attribute('href')[29:]: # 6
            pass
        if "politico.com" in url.get_attribute('href')[29:]: # 7
            pass
        if "yahoo.com/news" in url.get_attribute('href')[29:]: # 8
            pass
        if "npr.org" in url.get_attribute('href')[29:]: # 9
            pass
        if "latimes.com" in url.get_attribute('href')[29:]: # 10
            pass
    driver.save_screenshot('screen.png') # save a screenshot to disk to see what we're looking at
driver.quit()