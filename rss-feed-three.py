#############
# libraries #
#############

import datetime
import PyRSS2Gen
import requests
from bs4 import BeautifulSoup

############
# settings #
############

makeRSS = True  # unset if testing

# The name of the channel
channelTitle = "BBC Three"

# The URL to the HTML website corresponding to the channel.
channelLink = "http://www.bbc.co.uk/bbcthree"

# Phrase or sentence describing the channel.
channelDescription = "All the latest documentaries, comedy, videos, " \
                     "articles and more from the award winning digital " \
                     "channel, BBC Three. Makes you think. Makes you laugh."

# specify the url
three_page = 'http://www.bbc.co.uk/bbcthree'

#######################
# BeautifulSoup setup #
#######################

# query the website and return the html to the variable ‘page’
request = requests.get(three_page)
# print(request.encoding)
page = request.text

# parse the html using beautiful soup and store in variable `soup`
# soup = BeautifulSoup(page, 'html.parser')
soup = BeautifulSoup(page, 'lxml')

########################
# initialise variables #
########################

urls = []
titles = []
dictForRSS = {}

##########################
# extract promo elements #
##########################

promo_list = soup.findAll('a', attrs={'class': 'Promo--long-article'})
for promo in promo_list:

    # extract href contents
    url = promo['href']
    titlesRaw = promo.findAll('h3', text=True)

    # clean up h3 element to leave only heading
    for title in titlesRaw:
        title = title.text.strip()  # strip() is used to remove starting and trailing
        titles.append(title)

    # for the bits we've found, append them to the two empty lists
    urls.append(url)

##############
# RSS setup ##
##############

# See: channel required elements -- see https://cyber.harvard.edu/rss/rss.html for extended list
# See: see https://pypi.python.org/pypi/PyRSS2Gen for building feed

RSSItemList = []
for Title, Link in zip(titles, urls):
    RSSItemList.append(PyRSS2Gen.RSSItem(
        title=Title, link=Link,
        guid=PyRSS2Gen.Guid(Link)))

if makeRSS:
    rss = PyRSS2Gen.RSS2(
        title=channelTitle,
        link=channelLink,
        description=channelDescription,
        generator="BBC Three RSS generator",
        docs="http://cyber.harvard.edu/rss/rss.html",
        lastBuildDate=datetime.datetime.now(),
        items=RSSItemList
    )

    rss.write_xml(open("bbc-three-rss.xml", "w", encoding="utf-16"))  # encoding very important, breaks otherwise!