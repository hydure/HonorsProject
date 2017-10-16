# found out how to not display web browser when using selenium here:
# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

# TODO: Look at pp. 264 - 275 for further information regarding Flask-based web apps
# TODO: 
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from string import Template
import time
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

class SearchForm(Form):
    inputString = TextAreaField('', [validators.DataRequired()])

@app.route('/')
def index():
    form = SearchForm(request.form)
    return render_template('Website.html')

@app.route('/', methods=['POST'])
def results():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        inputString = request.form['inputString']

        driver = webdriver.PhantomJS()  # Creates an invisible browser
        driver.get('https://google.com/') # Navigates to Google.com
        searchBarInput = driver.find_element_by_name('q') # Assigns variable to Google Search bar
        if inputString != '':
            searchBarInput.send_keys(inputString) # what you are searching for
            searchBarInput.send_keys(Keys.RETURN) # Hit <RETURN> so Google begins searching
            time.sleep(1) # sleep for a bit so the results webpage will be rendered

            # scrape first liberal and first conservative websites that are in the top 10 news websites
            # (top 10 according to http://blog.feedspot.com/usa_news_websites/ 's metrics)
            urls = driver.find_elements_by_css_selector('h3.r a')
            conservativeURL = ' '
            liberalURL = ' '

            # Continue mining until conservative- and liberalURL are found
            while conservativeURL == ' ' or liberalURL == ' ':
                urls = driver.find_elements_by_css_selector('h3.r a')
                for url in urls:
                    # TODO: scrape according to each website's layout and then run ML algorithm
                    if conservativeURL != ' ' and liberalURL != ' ':
                        break
                    stoppingPoint = url.get_attribute('href').index('&')
                    url = url.get_attribute('href')[29 : stoppingPoint]
                    print(url)
                    if '?q=' in url:
                        continue
                    if "cnn.com" in url: # 1
                        cLinkName = "CNN Article"
                        conservativeURL = url
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('div', {"class":"zn-body__paragraph"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                    if "nytimes.com" in url: # 2
                        lLinkName = "NY Times Article"
                        liberalURL = url
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p', {"class":"story-body-text story-content"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                    if "huffingtonpost.com" in url: # 3
                        pass
                    if "foxnews.com" in url: # 4
                        pass
                    if "usatoday.com" in url: # 5
                        pass
                    if "reuters.com" in url: # 6
                        pass
                    if "politico.com" in url: # 7
                        pass
                    if "yahoo.com/news" in url: # 8
                        pass
                    if "npr.org" in url: # 9
                        pass
                    if "latimes.com" in url: # 10
                        pass
                    if "washingtonpost.com" in url: # requested
                        pass

                if conservativeURL != ' ' and liberalURL != ' ':
                    break

                # Go to the next page to continue the process
                nextPage = driver.find_element_by_link_text("Next").click()
            
            driver.save_screenshot('screen.png') # save a screenshot to disk to see what we're looking at
        driver.quit()

    return render_template('Website.html', cLinkName=cLinkName, lLinkName=lLinkName, \
                            conservativeURL=conservativeURL, liberalURL=liberalURL)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# Had trouble accessing the google news search element and there was no supporting, non-deprecated info for it
# results found looking from the first result in the first result page and continue sequentially. Results are found
# by Google's algorithm to generate the most "relevant" results related to the search query