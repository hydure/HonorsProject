# TODO: Scrape articles from the HuffingTon Post (liberal), (Bannon @ Brietbart), NY Times, NY Post (check opinion polls first)
# TODO: Look up YouTube API and scrape Colbert, Trevor Noah, Seth Meyers (Get article about how liberal talk show hosts are for support)
# TODO: Bill Maher for funzies, Jimmy Kimmel for moderate...look for more later

import requests
from bs4 import BeautifulSoup
import csv
import sys

listName = [None] * integer

# Specify where you want the URL links to be stored and read from
fileStoringURLs = "URLFile.csv"

#######################################################################################

def readCSV(csv):

    # Read CSV of URLs
    sourceFile = open(fileStoringURLs, "r")
    reader = csv.reader(sourceFile)

    row = 0
    for line in reader:
        # Save header row
        if row == 0:
            header = line
            row = 1
        else:
            col = 0
            for column in line:
                print("{} : {}".format(header[col], column))
                col += 1

#######################################################################################

def createCSVFile():
    # Write CSV Header
    csv = open(fileStoringURLs, "w")
    colTitleRow = "URL Links\n"
    csv.write(colTitleRow)
    return csv

#######################################################################################

def getLimbaughTranscripts(csv):
    # Collects all transcript links from Rush Limbaugh's show up to archives/page/501
    for x in range(1, 502):
        result = requests.get("https://www.rushlimbaugh.com/archives/page/{}/".format(x))
        soup = BeautifulSoup(result.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            if "daily" in str(link.get("href")):
                # Excludes all of the URLs that are not articles 
                if len(str(link.get("href"))) > 46:
                    csv.write(link.get("href") + "\n")
                #print("<a href='%s'>%s</a>" % (link.get("href"), link.text))

#######################################################################################

def getIngrahamTranscripts(csv):
    # Collects all transcript links from Laura Ingraham's show
    for x in range(15, 136, 15):
        result = requests.get("https://www.lauraingraham.com/#start={}".format(x))
        soup = BeautifulSoup(result.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            # Excludes all of the URLs that are not articles
            if "/b/" in str(link.get("href")):
                #print("https://www.lauraingraham.com" + link.get("href") + "\n")
                csv.write("https://www.lauraingraham.com" + link.get("href") + "\n")

#######################################################################################

def getTheFiveTranscripts(csv):
    # Collects all transcript links from Fox New's The Five
    for x in range(1, 181):
        result = requests.get("http://www.foxnews.com/on-air/the-five/transcripts?page={}".format(x))
        soup = BeautifulSoup(result.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            # Excludes all of the URLs that are not articles
            if "transcript" in str(link.get("href")) and len(str(link.get("href"))) > 29:
               #print(link.get("href"))
               csv.write(link.get("href") + "\n")

#######################################################################################

def getHannityTranscripts(csv):
    # Collects all transcript links from Sean Hannity's show
    for x in range(1, 300):
        result = requests.get("http://www.foxnews.com/on-air/hannity/transcripts?page={}".format(x))
        soup = BeautifulSoup(result.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            # Excludes all of the URLs that are not articles
            if "transcript" in str(link.get("href")) and len(str(link.get("href"))) > 29:
                #print(link.get("href"))
                csv.write(link.get("href") + "\n")

#######################################################################################

def getCoulterTranscripts(csv):
    # Collects all transcript links from Ann Coulter's show
    result = requests.get("http://www.anncoulter.com/archives.html")
    soup = BeautifulSoup(result.content, "html.parser")
    links = soup.find_all("a")

    for link in links:
        # Excludes all of the URLs that are not articles
        if "columns" in str(link.get("href")):
            #print("http://www.anncoulter.com" + link.get("href"))
            csv.write("http://www.anncoulter.com" + link.get("href") + "\n")

#######################################################################################

def getConservativeHostTranscripts(csv):
    getLimbaughTranscripts(csv)
    getIngrahamTranscripts(csv)
    getTheFiveTranscripts(csv)
    getHannityTranscripts(csv)
    getCoulterTranscripts(csv)

#######################################################################################

def getRachelMaddowTranscripts(csv):
    # Collects all the transcript links from Maddow's show
    for x in range(2008, 2018):
        for y in range(1, 13):
            result = requests.get("http://www.msnbc.com/transcripts/rachel-maddow-show/{}/{}".format(x, y))
            soup = BeautifulSoup(result.content, "html.parser")
            links = soup.find_all("a")

            for link in links:
                if "/transcripts/rachel-maddow-show/" in str(link.get("href")):
                    if len(str(link.get("href"))) > 40:
                        #print(link.get("href"))
                        csv.write("http://www.msnbc.com" + link.get("href") + "\n")

#######################################################################################

def getLiberalHostTranscripts(csv):
    # TODO: Write get functions for 4 more liberal hosts
    getRachelMaddowTranscripts(csv)

#######################################################################################

def grabURLs():
    csv = createCSVFile()
    getConservativeHostTranscripts(csv)
    print("Grabbed all conservative URLs!")
    getLiberalHostTranscripts(csv)
    print("Grabbed all URLs!")
    # TODO: Open each URL and then scrap off text...MAY VARY BETWEEN WEBSITE!!!!!!

#grabURLs()
