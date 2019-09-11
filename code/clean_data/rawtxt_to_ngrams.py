from nltk.stem import PorterStemmer
import pandas as pd 
import os, sys

###########################################################################
# Storage
###########################################################################

BASE_DIR = '/Users/stevelee/Dropbox/CourseWork/Fall2019/DataScience/project/'
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_FILE = os.path.join(DATA_DIR, 'articles.csv')
CLEAN_DATA_FILE = os.path.join(DATA_DIR, 'ngram_articles.csv')
STOP_WORDS = os.path.join(BASE_DIR, 'code', 'clean_data', 'stopwords.txt')
ps = PorterStemmer()

###########################################################################
# Functions
###########################################################################

def only_alphas(txt):
    txt = str(txt)
    txt = txt.replace('Video', '').replace('\n', ' ').replace('--', ' ')
    t = [i.lower() for i in txt if i.isalpha() or i == ' ']
    return ''.join(t)

def get_stop_words():
    with open(STOP_WORDS, 'r') as f: 
        txt = f.read()
    return txt.split('\n')

def remove_stop_words(txt, stop_words): 
    txt = txt.split(' ')
    return ' '.join([w.strip() for w in txt if ((w not in stop_words) and (w != ' ') and (w != '')) ])

def stem(txt): 
    global ps
    txt = txt.split(' ')
    return ' '.join([ps.stem(w) for w in txt])

def ngrams(txt, n_gram=1):
    '''
    INPUT   : txt    -> text in alpha only, stemmed, form
            : n_gram -> the length of each phrase to generate
    OUTPUT  : a string of ngram phrases
    '''
    token = [t for t in txt.split(' ')]
    ngrams = zip(*[token[i:] for i in range(n_gram)])
    ngrams_lst = [' '.join(g) for g in ngrams]
    return '.'.join(ngrams_lst)

###########################################################################
# Main
###########################################################################

if __name__ == '__main__':

    # read raw text data 

    print('Reading data...')
    df = pd.read_csv(RAW_DATA_FILE, sep='|').drop('Unnamed: 0', axis=1)

    # remove all non alpha characters 

    print('Removing all non alpha characters...')
    df['article_alpha'] = df['article'].apply(only_alphas)
    df = df.drop('article', axis=1)

    # remove stopwords 
    
    print('Removing stop words...')
    stop_words = get_stop_words()
    df['article_no_stop'] = df['article_alpha'].apply(remove_stop_words, args=[stop_words])
    df = df.drop('article_alpha', axis=1)

    # stem 
    
    print('Stemming...')
    df['articles_stemmed'] = df['article_no_stop'].apply(stem)
    df = df.drop('article_no_stop', axis=1)
    
    # generate n-grams
    
    print('Generating ngrams...')
    df['1-gram'] = df['articles_stemmed'].apply(ngrams, args=[1])
    df['2-gram'] = df['articles_stemmed'].apply(ngrams, args=[2])
    df['3-gram'] = df['articles_stemmed'].apply(ngrams, args=[3])

    # save 
    
    print('Saving...')
    df.to_csv(CLEAN_DATA_FILE, sep='|')
    print('Saved.')