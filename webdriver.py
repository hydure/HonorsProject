# found out how to not display web browser when using selenium here:
# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768) # optional
driver.get('https://google.com/')

searchBarInput = driver.find_element_by_name('q')
searchBarInput.send_keys("")
searchBarInput.send_keys(Keys.RETURN)
time.sleep(3)
# scrape first two websites
#check if one website is liberal and the other is conservative, if not scape the next website until requirements are met (probably use flags)
driver.save_screenshot('screen.png') # save a screenshot to disk to see what we're looking at
driver.quit()