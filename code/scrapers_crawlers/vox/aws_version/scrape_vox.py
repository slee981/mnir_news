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
ENTERTAINMENT_FOLDER = 'vox-culture'
POLITICS_FOLDER      = 'vox-politics'
TECH_FOLDER          = 'vox-tech'

ARTICLES_PER_TOPIC = 2000

CULTURE = []
POLITICS = []
TECH = []

TOPICS = {"politics": POLITICS, "culture": CULTURE, "tech": TECH}

CHROME_PATH = "/usr/bin/chromedriver"

########################################
# Functions
########################################

def scrape(url, browser=None, file_id=None, last_article=True, relevant_topics=None):
    '''
    Motivation
      - this function should take a vox news url,
        scrape the text, and write a txt file
        into a corresponding folder.

    Input
      - a vox news url to scrape
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
        relevant_topics = ['politics', 'culture', 'tech']

    try:
        browser.get(url)
    except:
        print(f'\n[!!!] ERROR: Cannot get {url}\n')
        browser.quit()
        browser = webdriver.Chrome(CHROME_PATH)
        browser.implicitly_wait(15)
        return False

    # unique xpath to get text for vox news
    try:
        contents = browser.find_elements_by_xpath('/html/body/div/section/section/div[2]/div[1]/div[1]')
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
      - vox news adds random shit in 'strong'
        and 'blockquote' brackets that are
        not really part of the article

    Input
      - the article contents webdriver object

    Output
      - a string of cleaned text
    '''

    text = article_contents[0].text

    headers = article_contents[0].find_elements_by_tag_name('h3')
    tweets  = article_contents[0].find_elements_by_tag_name('twitter-widget')
    
    for h in headers: 
        text = text.replace(h.text, '')

    for tweet in tweets:
        text = text.replace(tweet.text, '')

    # remove the word Vox and VOX from the text
    if "Vox News" in text:
        text = text.replace("Vox News", '')
    if "VOX" in text:
        text = text.replace("VOX", '')
    if "Vox's" in text:
        text = text.replace("Vox's", '')
    if "Vox" in text:
        text = text.replace("Vox", '')
    if 'vox.com' in text: 
        text = text.replace("vox.com", '')
    if 'vox' in text: 
        text = text.replace("vox", '')
    

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
        loaded vox news article

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

            if ('auth.voxmedia' in addr): 
                continue

            if ('policy-and-politics/2' in addr) \
                and ('politics' in relevant_topics) \
                and addr not in TOPICS['politics']:

                TOPICS['politics'].append(addr)
                new_urls += 1

            elif ('culture/2' in addr) \
                and ('culture' in relevant_topics) \
                and addr not in TOPICS['culture']:

                TOPICS['culture'].append(addr)
                new_urls += 1

            elif ('technology/2' in addr) \
                and ('technology' in relevant_topics) \
                and addr not in TOPICS['tech']:

                TOPICS['tech'].append(addr)
                new_urls += 1

    print(f"  -> Added {new_urls} new urls")

def get_correct_folder(url):

    folder = BASE_FOLDER

    if 'politics/' in url:
        folder += POLITICS_FOLDER

    elif 'culture' in url:
        folder += ENTERTAINMENT_FOLDER

    elif 'tech' in url:
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

    # folder is formatted "/home/stephen/.../vox-topic"
    topic = folder[len(BASE_FOLDER)+4:]

    file_name = f"vox_{topic}_{file_id}.txt"
    with open(file_name, 'a') as f:
        f.write(text)

    with open('urls.txt', 'a') as f: 
        f.write(f"{url}|*|")

    print(f"wrote {file_name}")

def get_starter_urls():

    folder = './starter-urls/'
    politics = 'politics.txt'
    culture = 'culture.txt'
    tech = 'tech.txt'
    files = [politics, culture, tech]

    os.chdir(folder)
    for url_file in files:
        with open(url_file, 'r') as f: 
            urls = f.read()
            urls = urls.split("|*|")
            urls = [url for url in urls if len(url) > 0]
            
        if 'politics' in url_file: 
            TOPICS['politics'].extend(urls)
        elif 'culture' in url_file: 
            TOPICS['culture'].extend(urls)
        elif 'tech' in url_file: 
            TOPICS['tech'].extend(urls)

    os.chdir("../")

def main():

    # read in starter urls
    get_starter_urls()

    display = Display(visible=0, size=(800,1200))
    display.start()
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
            current_url += 1
            
            if ("vox" not in url) or ('auth.voxmedia' in url): 
                continue 

            if scrape(url, browser=browser, file_id=articles_scraped, last_article=False, relevant_topics=relevant_topics):

                articles_scraped +=  1

            print(f'  -> {len(TOPICS[topic]) - current_url} urls left in this topic')
            print(f"  -> relevant url topics {relevant_topics}")

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
