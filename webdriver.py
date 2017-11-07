# found out how to not display web browser when using selenium here:
# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

# TODO: Run scraped texts against ML algorithm to generate a number in checkURL
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, TextAreaField, validators
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from string import Template
import time, requests, numpy
from bs4 import BeautifulSoup

# Made these global so both @app.route functions and checkURL can access them
conservativeURL   = ' '
liberalURL        = ' '
cLinkName         = ' '
lLinkName         = ' '
errMessage        = ' '
loadedModel       = load_model('finalizedModel.h5')
MAX_REVIEW_LENGTH = 500
TOP_WORDS = 5000                # Most-used words in the article.

# TODO: Run text through algorithm and determine if url should fill either conservative
#       or liberal URL spots on webpage (will need to determine threshold values)
def checkURL(url, text, linkName):
    global conservativeURL
    global liberalURL
    global cLinkName
    global lLinkName

    # Preprocess article to predict its political bias
    tokenizer = Tokenizer(num_words=TOP_WORDS, split=' ')
    tokenizer.fit_on_texts([text])
    X = tokenizer.texts_to_sequences([text])
    X = pad_sequences(X)
    print("Article has been preprocessed and a prediction is being made...")

    #TODO: Figure out prediction
    
    if True:
    
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
    return render_template('Website.html', cLinkName=cLinkName, lLinkName=lLinkName, \
                            conservativeURL=conservativeURL, liberalURL=liberalURL, \
                            errMessage=errMessage)

@app.route('/results', methods=['GET', 'POST'])
def results():
    global conservativeURL
    global liberalURL
    global cLinkName
    global lLinkName
    global errMessage
    global tokenizer

    # Need to clear these fields to run another query
    conservativeURL = ' '
    liberalURL      = ' '
    cLinkName       = ' '
    lLinkName       = ' '
    errMessage      = ' '
    
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
                        linkName = "Huffington Post Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p', {"class":"p1"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
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
                        #print(text)
                        checkURL(url, text, linkName)

                    if "usatoday.com" in url: # 5
                        linkName = "USA Today Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p', {"class":"p-text"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                        checkURL(url, text, linkName)

                    if "reuters.com" in url: # 6
                        linkName = "Reuters Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p')
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        text = text[:-36]
                        #print(text)
                        checkURL(url, text, linkName)

                    if "politico.com" in url: # 7
                        linkName = "Politico Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p')
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                        checkURL(url, text, linkName)

                    if "yahoo.com/news" in url and "tagged" not in url: # 8
                        linkName = "Yahoo! News Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p', {"class":"canvas-atom"})
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                        checkURL(url, text, linkName)

                    if "npr.org" in url: # 9
                        linkName = "NPR Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p')
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        text = text[:-44]
                        #print(text)
                        checkURL(url, text, linkName)

                    if "latimes.com" in url: # 10
                        linkName = "LA Times Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p')
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                        checkURL(url, text, linkName)

                    if "washingtonpost.com" in url: # requested
                        linkName = "Washington Post Article"
                        lookAtPage = requests.get(url)
                        soup = BeautifulSoup(lookAtPage.text, "html.parser")
                        paragraphs = soup.find_all('p')
                        text = ''
                        for paragraph in paragraphs:
                            text = text + paragraph.text
                        #print(text)
                        checkURL(url, text, linkName)

                if conservativeURL != ' ' and liberalURL != ' ':
                    break

                # Go to the next page to continue the process
                try:
                    nextPage = driver.find_element_by_link_text("Next").click()
                except:
                    errMessage = "Could not find enough sources on topic."
                    break                    
            
            #driver.save_screenshot('screen.png') # save a screenshot to disk to see what we're looking at
        driver.quit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# Had trouble accessing the google news search element and there was no supporting, non-deprecated info for it
# results found looking from the first result in the first result page and continue sequentially. Results are found
# by Google's algorithm to generate the most "relevant" results related to the search query