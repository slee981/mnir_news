########################################
# Imports
########################################
import requests as req
from selenium import webdriver
from pyvirtualdisplay import Display
import sys

import os    # os.chdir('/home/stephen/...')
             # os.getcwd()

########################################
# Constants
########################################
BASE_FOLDER          = '/home/ubuntu/efs/'
ENTERTAINMENT_FOLDER = 'fox-entertainment'
POLITICS_FOLDER      = 'fox-politics'
TECH_FOLDER          = 'fox-tech'

BASE_URL = 'www.foxnews.com/'
START_URL = 'https://www.foxnews.com/politics/sen-cotton-unloads-on-aocs-green-new-deal-says-media-helped-to-cover-up-most-radical-parts-of-proposal'
TECH_URL = 'https://www.foxnews.com/tech/ex-facebook-executive-slams-amazon-says-theres-no-limit-to-alexa-storing-and-listening-to-private-conversations'

ARTICLES_PER_TOPIC = 2000

ENTERTAINMENT = []
POLITICS = [START_URL]
TECH = [TECH_URL]

TOPICS = {"politics": POLITICS, "entertainment": ENTERTAINMENT, "tech": TECH}

CHROME_PATH = "/usr/bin/chromedriver"

########################################
# Functions
########################################

def scrape(url, browser=None, file_id=None, last_article=True, relevant_topics=None):
    '''
    Motivation
      - this function should take a fox news url,
        scrape the text, and write a txt file
        into a corresponding folder.

    Input
      - a fox news url to scrape
      - a file id to save it (optional)
      - a selenium webdriver (optional)

    Output
      - a txt file written to appropriate folder
    '''

    if browser == None:
        try:
            browser = webdriver.Chrome(CHROME_PATH)
        except:
            display = Display(visible=0, size=(800,1200))
            display.start()
            browser = webdriver.Chrome(CHROME_PATH)
        finally:
            browser.implicitly_wait(15)

    if file_id == None:
        file_id = 1

    if relevant_topics == None:
        relevant_topics = ['politics', 'entertainment', 'tech']

    try:
        browser.get(url)
    except:
        print(f'\n[!!!] ERROR: Cannot get {url}\n')
        browser.refresh()
        return False

    # unique xpath to get text for fox news
    try:
        contents = browser.find_elements_by_xpath('//*[@id="wrapper"]/div[2]/div[1]/main/article/div/div/div[1]')
    except:
        print(f"Error getting xpath {url}")
        return False

    try:
        text = get_clean_txt(contents)
    except:
        print(f"Error cleaning text in {url}")
        return False

    try:
        get_relevant_urls(browser, relevant_topics)
    except:
        print("error getting urls")
        return False

    try:
        topic_folder = get_correct_folder(url)
        write_txt_file(text, url, file_id, topic_folder)
    except:
        print("error writing")
        return False

    if last_article:
        browser.quit()

    return True

def get_clean_txt(article_contents):
    '''
    Motivation
      - fox news adds random shit in 'strong'
        and 'blockquote' brackets that are
        not really part of the article

    Input
      - the article contents webdriver object

    Output
      - a string of cleaned text
    '''
    text = article_contents[0].text

    # try to get the ugly children
    blockquote_txt    = article_contents[0].find_elements_by_class_name('quote-text')
    blockquote_author = article_contents[0].find_elements_by_class_name('quote-author')
    strong            = article_contents[0].find_elements_by_tag_name('strong')
    bold              = article_contents[0].find_elements_by_tag_name('b')

    tweets             = article_contents[0].find_elements_by_tag_name('twitter-widget')
    for tweet in tweets:
        text = text.replace(tweet.text, '')

    for s in strong:
        try:
            a_txt = s.find_element_by_tag_name('a')
            text = text.replace(a_txt.text, '')
        except:
            text = text.replace(s.text, '')

    for author in blockquote_author:
        text = text.replace(author.text, '')

    for txt in blockquote_txt: 
        text = text.replace(txt.text, '')

    for b in bold:
        text = text.replace(b.text, '')

    # remove the word Fox and FOX from the text
    if "Fox & Friends" in text:
        text = text.replace("Fox & Friends", '')
    if "Fox News" in text:
        text = text.replace("Fox News", '')
    if "FOX" in text:
        text = text.replace("FOX", '')
    if "Fox" in text:
        text = text.replace("Fox", '')

    return text

def get_relevant_urls(browser, relevant_topics=None):
    '''
    Motivation
      - this appends 'relevant' urls to
        an appropriate list. Relevant means that
        the url is unique and related to either
        politics, entertainment, or tech.

    Input
      - a live selenium webdriver instance with
        loaded fox news article

    Output
      - none
    '''

    if relevant_topics == None:
        relevant_topics = ['politics', 'entertainment', 'tech']

    anchors = browser.find_elements_by_tag_name('a')

    new_urls = 0
    for a in anchors:
        addr = a.get_attribute('href')

        if (BASE_URL + 'politics/' in addr) \
            and ('print' not in addr) \
            and ('politics' in relevant_topics) \
            and addr not in TOPICS['politics']:

            TOPICS['politics'].append(addr)
            new_urls += 1

        elif (BASE_URL + 'entertainment/' in addr) \
            and ('print' not in addr) \
            and ('entertainment' in relevant_topics) \
            and addr not in TOPICS['entertainment']:

            TOPICS['entertainment'].append(addr)
            new_urls += 1

        elif (BASE_URL + 'tech/' in addr) \
            and ('print' not in addr) \
            and ('tech' in relevant_topics) \
            and addr not in TOPICS['tech']:

            TOPICS['tech'].append(addr)
            new_urls += 1

    print(f"  -> Added {new_urls} new urls")

def get_correct_folder(url):

    folder = BASE_FOLDER

    if BASE_URL + 'politics/' in url:
        folder += POLITICS_FOLDER

    elif BASE_URL + 'entertainment/' in url:
        folder += ENTERTAINMENT_FOLDER

    elif BASE_URL + 'tech/' in url:
        folder += TECH_FOLDER

    else:
        raise ValueError

    return folder

def write_txt_file(text, url, file_id, folder):
    '''
    Motivation
      - this function takes text and writes
        it as a text file into an appropriate
        folder

    Input
      - text from article
      - file id number
      - topic category
        --> entertainment
        --> politics
        --> tech

    Output
      - none
    '''

    os.chdir(folder)

    # folder is formatted "~/fox-topic"
    topic = folder[len(BASE_FOLDER)+4:]

    file_name = f"fox_{topic}_{file_id}.txt"
    with open(file_name, 'a') as f:
        f.write(text)
    
    with open("urls.txt", 'a') as f: 
        f.write(f"|*|{file_id}: '{url}'")

    print(f"wrote {file_name}")

def main():
    display = Display(visible=0, size=(800,1200))
    display.start()
    browser = webdriver.Chrome(CHROME_PATH)
    browser.implicitly_wait(15)

    topics = [topic for topic in TOPICS.keys()]
    for i, topic in enumerate(topics):
        print(f'\n*** looking for {topic} ***\n')

        # set relevant topics to avoid unnecessary url hunting
        ### use this to get all topcis
        # relevant_topics = topics[i:]

        # this will only get politics 
        relevant_topics = 'politics'

        # reset counters for each topic
        articles_scraped = 0
        current_url = 0

        # loop as long as there are enough new urls
        while len(TOPICS[topic]) > current_url and articles_scraped < ARTICLES_PER_TOPIC:
            url = TOPICS[topic][current_url]

            if scrape(url, browser=browser, file_id=articles_scraped, last_article=False, relevant_topics=relevant_topics):

                articles_scraped +=  1

            print(f'  -> {len(TOPICS[topic]) - current_url} urls left in this topic')
            print(f"  -> relevant url topics {relevant_topics}")
            current_url  +=  1

    browser.quit()

def test(url):
    scrape(url, file_id="test")

########################################
# Main
########################################
if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        write_txt_file('hello', 'test_url', 'file_id', '/home/ubuntu/efs/fox-politics')

    elif len(sys.argv) == 2:
        url = sys.argv[1]
        test(url)
    else:
        main()
