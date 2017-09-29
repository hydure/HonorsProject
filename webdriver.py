# found out how to not display web browser when using selenium here:
# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

# TODO: Look at pp. 264 - 275 for further information regarding Flask-based web apps
# TODO: 
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from string import Template

app = Flask(__name__)

class SearchForm(Form):
    inputString = TextAreaField('', [validators.DataRequired()])

@app.route('/')
def index():
    form = SearchForm(request.form)
    return render_template('Website.html', form=form)

@app.route('/', methods=['POST'])
def results():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        inputString = request.form['inputString']

        driver = webdriver.PhantomJS()  # Creates an invisible browser
        driver.get('https://google.com/') # Navigates to Google.com

        searchBarInput = driver.find_element_by_name('q') # Assigns variable to Google Search bar
        if inputString != '':
            searchBarInput.send_keys(inputString + " news") # what you are searching for
            searchBarInput.send_keys(Keys.RETURN) # Hit <RETURN> so Google begins searching
            time.sleep(1) # sleep for a bit so the results webpage will be rendered

            # TODO: scrape first two websites that are in the top 10 news websites
            #       (top 10 according to http://blog.feedspot.com/usa_news_websites/ 's metrics)
            urls = driver.find_elements_by_css_selector('h3.r a')
            conservativeURL = ' '
            liberalURL = ' '
            test = None
            # TODO: Make it go to the next page and continue mining until 
            #while conservativeURL != ' ' and liberalURL != ' ':
            for url in urls:
                # TODO: scrape according to each website's layout and then run ML algorithm
                # TODO: check if one website is liberal and the other is conservative,
                #       if not scape the next website until requirements are met
                test = url
                if conservativeURL != ' ' and liberalURL != ' ':
                    break
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
                
            conservativeURL = test
            liberalURL = test
            
            driver.save_screenshot('screen.png') # save a screenshot to disk to see what we're looking at
        driver.quit()

    return render_template('Website.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)