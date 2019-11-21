from bs4 import BeautifulSoup
import requests
import pprint

p = pprint.PrettyPrinter(indent=4).pprint

rootUrl = 'https://www.ecosophia.net/tag/the-cosmic-doctrine/'
urlPrefix = 'https://www.ecosophia.net/'
blogPrefix = 'the-cosmic-doctrine'

def createSoup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')

def getReadMoreLinks(url):
    soup = createSoup(url)
    readMoreLinks = soup.find_all('a', class_='readMoreLink')
    links = []
    for link in readMoreLinks:
        if link is not None:
            href = link['href']
            splitted = href.split(urlPrefix)
            if splitted[1].startswith(blogPrefix):
                links.append(href)
    return links

def getNextPageHref (url):
    soup = createSoup(url)
    nextPageEl = soup.find('a', class_='next page-numbers')
    if nextPageEl is not None:
        return nextPageEl['href']

def getSubLinks(rootUrl):
    url = getNextPageHref(rootUrl)
    subLinks = []
    while url is not None:
        subLinks.append(url)
        url = getNextPageHref(url)
    return subLinks

def getPageText(url):
    soup = createSoup(url)
    return soup.get_text()

def main():    
    # get all top level pages
    links = getSubLinks(rootUrl)
    # insert root url into list
    links.insert(0, rootUrl)
    # reverse list to order older content as first
    links.reverse()
    readMoreLinks = []
    # for each url, get all readMoreLinks
    for link in links:
        readLinks = getReadMoreLinks(link)
        readLinks.reverse()
        readMoreLinks.extend(readLinks)
    # for each readMoreLink, get all text data from link
    text_file = open("Output.txt", "w")
    for link in readMoreLinks:
        text = getPageText(link)
        # write text to text file
        text_file.write(text)
    text_file.close()

main()

