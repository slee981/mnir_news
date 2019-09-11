########################################
# Imports
########################################
import requests as req
from selenium import webdriver
import sys

import os    # os.chdir('/home/stephen/...')
             # os.getcwd()

########################################
# Constants
########################################
BASE_FOLDER          = '/home/stephen/Dropbox/CodeWorkspace/python/news-article-scraper/pbs/'
ENTERTAINMENT_FOLDER = 'pbs-culture'
POLITICS_FOLDER      = 'pbs-politics'
TECH_FOLDER          = 'pbs-tech'

ARTICLES_PER_TOPIC = 3

CULTURE = ['https://www.pbs.org/newshour/arts/at-the-end-of-a-bumpy-year-2019-oscars-may-reward-a-hollywood-disrupter']
POLITICS = ['https://www.pbs.org/newshour/politics/a-federal-court-cant-count-vote-of-deceased-judge-supreme-court-rules']
TECH = ['https://www.pbs.org/newshour/science/in-search-of-lifes-origins-japans-hayabusa-2-spacecraft-lands-on-an-asteroid', 'https://www.pbs.org/newshour/science/how-smallpox-devastated-the-aztecs-and-helped-spain-conquer-an-american-civilization-500-years-ago']

TOPICS = {"politics": POLITICS, "culture": CULTURE, "tech": TECH}

CHROME_PATH = "/usr/lib/chromium-browser/chromedriver"

########################################
# Functions
########################################

def scrape(url, browser=None, file_id=None, last_article=True, relevant_topics=None):
    '''
    Motivation
      - this function should take a pbs news url,
        scrape the text, and write a txt file
        into a corresponding folder.

    Input
      - a pbs news url to scrape
      - a file id to save it (optional)
      - a selenium webdriver (optional)

    Output
      - a txt file written to appropriate folder
    '''

    if browser == None:
        browser = webdriver.Chrome(CHROME_PATH)

    if file_id == None:
        file_id = 1

    if relevant_topics == None:
        relevant_topics = ['politics', 'culture', 'tech']

    try:
        browser.get(url)
    except:
        print(f'\n[!!!] ERROR: Cannot get {url}\n')
        browser.refresh()
        return False

    # unique xpath to get text for pbs news
    try:
        contents = browser.find_elements_by_class_name('body-text')
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
      - pbs news adds random shit in 'strong'
        and 'blockquote' brackets that are
        not really part of the article

    Input
      - the article contents webdriver object

    Output
      - a string of cleaned text
    '''

    text = article_contents[0].text
    asides = article_contents[0].find_elements_by_tag_name('aside')
    tweets  = article_contents[0].find_elements_by_tag_name('twitter-widget')
    
    for tweet in tweets:
        text = text.replace(tweet.text, '')

    for aside in asides: 
        text = text.replace(aside.text, '')

    # remove the word PBS from the text
    if "PBS" in text:
        text = text.replace("PBS", '')
    if 'pbs.com' in text: 
        text = text.replace("pbs.com", '')
    if 'pbs' in text: 
        text = text.replace("pbs", '')

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
        loaded pbs news article

    Output
      - none
    '''

    if relevant_topics == None:
        relevant_topics = ['politics', 'culture', 'tech']

    anchors = browser.find_elements_by_tag_name('a')

    new_urls = 0
    for a in anchors:
        if a.get_attribute('href') != None:
            addr = a.get_attribute('href')

            if ('www.pbs.org/newshour/politics/' in addr) \
                and ('politics' in relevant_topics) \
                and addr not in TOPICS['politics']:

                TOPICS['politics'].append(addr)
                new_urls += 1

            elif ('www.pbs.org/newshour/arts/' in addr) \
                and ('culture' in relevant_topics) \
                and addr not in TOPICS['culture']:

                TOPICS['culture'].append(addr)
                new_urls += 1

            elif ('www.pbs.org/newshour/science/' in addr) \
                and ('technology' in relevant_topics) \
                and addr not in TOPICS['tech']:

                TOPICS['tech'].append(addr)
                new_urls += 1

    print(f"  -> Added {new_urls} new urls")

def get_correct_folder(url):

    folder = BASE_FOLDER

    if 'politics' in url:
        folder += POLITICS_FOLDER

    elif 'art' in url or 'show' in url:
        folder += ENTERTAINMENT_FOLDER

    elif 'science' in url:
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

    # folder is formatted "/home/stephen/.../pbs-topic"
    topic = folder[len(BASE_FOLDER)+4:]

    file_name = f"pbs_{topic}_{file_id}.txt"
    with open(file_name, 'a') as f:
        f.write(text)

    with open('urls.txt', 'a') as f: 
        f.write(f"{url}|*|")

    print(f"wrote {file_name}")

def get_starter_urls():

    folder = './starter-urls/'

    os.chdir(folder)
    with open('science-urls.txt', 'r') as f: 
            urls = f.read()
            urls = urls.split("|*|")

    # remove the last null value
    urls = urls[:-1]          
    TOPICS['tech'].extend(urls)
    os.chdir("../")

def main():

    # read in starter urls for science
    get_starter_urls()

    browser = webdriver.Chrome(CHROME_PATH)
    browser.implicitly_wait(15)

    topics = [topic for topic in TOPICS.keys()]
    for i, topic in enumerate(topics):
        print(f'\n*** looking for {topic} ***\n')

        # set relevant topics to avoid unnecessary url hunting
        relevant_topics = topics[i:]

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

    if len(sys.argv) == 2:
        url = sys.argv[1]
        test(url)
    else:
        main()
