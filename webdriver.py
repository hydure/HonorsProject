# found out how to not display web browser when using selenium here:
# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

from selenium import webdriver

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768) # optional
driver.get('https://google.com/')
# driver.save_screenshot('screen.png') # save a screenshot to disk to see what we're looking at
sbtn = driver.find_element_by_css_selector('button.gbqfba')
sbtn.click()