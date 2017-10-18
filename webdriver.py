# found out how to not display web browser when using selenium here:
# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

# TODO: Look at pp. 264 - 275 for further information regarding Flask-based web apps
# TODO: Run scraped texts against ML algorithm to generate a number in checkURL
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from string import Template
import time
import requests
from bs4 import BeautifulSoup

conservativeURL = ' '
liberalURL      = ' '
cLinkName       = ' '
lLinkName       = ' '


# TODO: Run text through algorithm and determine if url should fill either conservative
#       or liberal URL spots on webpage (will need to determine threshold values)
def checkURL(url, text, linkName):
    global conservativeURL
    global liberalURL
    global cLinkName
    global lLinkName
    if conservativeURL == ' ':
        conservativeURL = url
        cLinkName = linkName
    elif liberalURL == ' ':
        liberalURL = url
        lLinkName = linkName

app = Flask(__name__)

class SearchForm(Form):
    inputString = TextAreaField('', [validators.DataRequired()])

@app.route('/')
def index():
    form = SearchForm(request.form)
    return render_template('Website.html')

@app.route('/', methods=['POST'])
def results():
    global conservativeURL
    global liberalURL
    global cLinkName
    global lLinkName
    errMessage = ' '

    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        inputString = request.form['inputString']

        driver = webdriver.PhantomJS()    # Creates an invisible browser
        driver.get('https://google.com/') # Navigates to Google.com
        searchBarInput = driver.find_element_by_name('q') # Assigns variable to Google Search bar
        if inputString != '':
            searchBarInput.send_keys(inputString + " news") # what you are searching for
            searchBarInput.send_keys(Keys.RETURN) # Hit <RETURN> so Google begins searching
            time.sleep(1) # sleep for a bit so the results webpage will be rendered

            # scrape first liberal and first conservative websites that are in the top 10 news websites
            # (top 10 according to http://blog.feedspot.com/usa_news_websites/ 's metrics)
            urls = driver.find_elements_by_css_selector('h3.r a')

            # Continue mining until conservative- and liberalURL are found
            while conservativeURL == ' ' or liberalURL == ' ':
                urls = driver.find_elements_by_css_selector('h3.r a')
                for url in urls:
                    if conservativeURL != ' ' and liberalURL != ' ':
                        break

                    # Need to remove end of links that make some webpages impossible
                    # to link to via my webpage
                    stoppingPoint = url.get_attribute('href').index('&')
                    url = url.get_attribute('href')[29 : stoppingPoint]
                    print(url)

                    # The queried search page is a url and needs to be skipped
                    if '?q=' in url:
                        continue

                    if "cnn.com" in url: # 1
                        continue
                        #cLinkName = "CNN Article"
                        #conservativeURL = url
                        linkName = "CNN Article"
                        
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('div', {"class":"zn-body__paragraph"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                        checkURL(url, text, linkName)

                    if "nytimes.com" in url: # 2
                        continue
                        #lLinkName = "NY Times Article"
                        #liberalURL = url
                        linkName = "NY Times Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p', {"class":"story-body-text story-content"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        checkURL(url, text, linkName)
                        #print(text)

                    if "huffingtonpost.com" in url: # 3
                        continue
                        linkName = "Huffington Post Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p', {"class":"p1"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        print(text)
                        checkURL(url, text, linkName)

                    if "foxnews.com" in url: # 4
                        linkName = "Fox News Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p')
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        text = text[161:-162]
                        print(text)
                        checkURL(url, text, linkName)

                    if "usatoday.com" in url: # 5
                        pass
                        linkName = "USA Today Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        #checkURL(url, text, linkName)

                    if "reuters.com" in url: # 6
                        pass
                        linkName = "Reuters Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        #checkURL(url, text, linkName)

                    if "politico.com" in url: # 7
                        pass
                        linkName = "Politico Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        #checkURL(url, text, linkName)

                    if "yahoo.com/news" in url: # 8
                        pass
                        linkName = "Yahoo! News Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        #checkURL(url, text, linkName)

                    if "npr.org" in url: # 9
                        pass
                        linkName = "NPR Article"
                        #checkURL(url, text, linkName)

                    if "latimes.com" in url: # 10
                        pass
                        linkName = "LA Times Article"
                        #checkURL(url, text, linkName)

                    if "washingtonpost.com" in url: # requested
                        pass
                        linkName = "Washington Post Article"
                        #checkURL(url, text, linkName)

                if conservativeURL != ' ' and liberalURL != ' ':
                    break
                driver.save_screenshot('screen.png') 
                # Go to the next page to continue the process
                try:
                    nextPage = driver.find_element_by_link_text("Next").click()
                except:
                    errMessage = "Could not find enough sources on topic."
                    break                    
            
            driver.save_screenshot('screen.png') # save a screenshot to disk to see what we're looking at
        driver.quit()

    return render_template('Website.html', cLinkName=cLinkName, lLinkName=lLinkName, \
                            conservativeURL=conservativeURL, liberalURL=liberalURL, errMessage=errMessage)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# Had trouble accessing the google news search element and there was no supporting, non-deprecated info for it
# results found looking from the first result in the first result page and continue sequentially. Results are found
# by Google's algorithm to generate the most "relevant" results related to the search query