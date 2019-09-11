import pandas as pd 
from collections import defaultdict
import os

###########################################################################
# Storage
###########################################################################

# specs for matrix
MIN_ARTICLE_LENGTH = 100
N = 3
SOURCE_ONE = 'PBS'
SOURCE_TWO = 'Fox'
N_GRAMS = '{}-gram'.format(N)

# path info 
BASE_DIR = '/Users/stevelee/Dropbox/CourseWork/Fall2019/DataScience/project/'
DATA_DIR = os.path.join(BASE_DIR, 'data')
CLEAN_DATA_FILE = os.path.join(DATA_DIR, 'ngram_articles.csv')
FINAL_DATA_FILE = os.path.join(DATA_DIR, 'final_ngram_vocab_articles.csv')
MATRIX_VALUES_FILE = os.path.join(DATA_DIR, '{s1}_{s2}_{ngm}_gram_counts.csv'.format(s1=SOURCE_ONE.lower(),\
                                                                                     s2=SOURCE_TWO.lower(),\
                                                                                     ngm=N ))

# map ngram to counts for corpus and by source
TOTAL_COUNTS = defaultdict(int)
SOURCE_ONE_COUNTS = defaultdict(int)
SOURCE_TWO_COUNTS = defaultdict(int)
VOCAB_INDEX_DICT = defaultdict(int)
VOCAB = []

###########################################################################
# Functions
###########################################################################

def count_article_length(txt):
    # note that txt from the dataframe is ' ' separated 
    if isinstance(txt, float): 
        txt = ''
    return len(txt.split(' '))

def count_all(txt, cts_dict):
    if isinstance(txt, str):
        txt = txt.split('.')
    else: 
        txt = ['_']

    for i in txt:
        cts_dict[i] += 1

def get_top_ngrams(ngram_dict, n=10): 
    df = pd.DataFrame(sorted(ngram_dict.items(), key=lambda x: x[1])[::-1])
    df.columns = ['ngram', 'count']
    return df.head(n)

def create_vocab(cts_dict, vocab, index_dict, vocab_size=1000): 
    total_words = 0
    for word in sorted(cts_dict.items(), key=lambda x: x[1], reverse=True): 
        # here, word is a tuple of ('word', count)
        if total_words < vocab_size:
            vocab.append(word[0])
            index_dict[word[0]] = total_words 
            total_words += 1
        else: 
            return

def bag_of_ngrams(doc_ngrams, vocab, vocab_index_dict):
    '''
    INPUT   : doc_ngrams   -> '.' separated string of ngrams for a document
            : vocab        -> an ordered list of the corpus vocabulary
    OUTPUT  : bag          -> '.' separated string of integer counts
                                this uses the indicies of the vocabulary 
                                and counts the occurances
    '''  
    # check type, this happens if doc = NaN in pandas
    bag = ['0'] * len(vocab)             # <- empty bag
    if isinstance(doc_ngrams, float):
        return bag
    elif isinstance(doc_ngrams, str):
        doc_cts = defaultdict(int)
        doc = doc_ngrams.split('.')
        for ngram in doc: 
            doc_cts[ngram] += 1
        for ngram in doc_cts:
            vocab_index = vocab_index_dict.get(ngram, -1)
            if vocab_index != -1: 
                bag[vocab_index] = str(doc_cts[ngram])
        return '.'.join(bag)
    else: 
        print('Error with this document ngram: {}'.format(doc_ngrams))
        raise TypeError

def reconstruct_doc(doc_vocab, vocab):
    doc = [int(ele) for ele in doc_vocab.split('.')]
    for idx, ct in enumerate(doc):
        ngram = vocab[idx]
        print('{} '.format(ngram) * ct, end='')
    print() 


def construct_final_df(df_subset, vocab): 
    '''
    INPUT   : df_subset -> dataframe with columns = [
                                'article id', 'source', 'articles_stemmed', 
                                '1-gram', '2-gram', '3-gram', 'bag_of_ngrams'
                            ]
            : vocab     -> list of ordered vocab words

    OUTPUT  : df_final  -> dataframe with columns = [
                                'article_id', 'source', 'ngram_1', ...
                                , 'ngram_p'
                            ]
    '''
    df_source = df_subset[['source']].copy()
    df_counts = df_subset['bag_of_ngrams'].apply(lambda x: pd.Series([int(i) for i in x.split('.')])).copy()
    df_counts.columns = vocab
    return df_source.join(df_counts)

###########################################################################
# Main
###########################################################################

if __name__ == '__main__':

    # read data
    print('Reading data...')
    df = pd.read_csv(CLEAN_DATA_FILE, sep='|').drop('Unnamed: 0', axis=1).set_index('article id')

    # remove short articles 
    df['stemmed_count'] = df['articles_stemmed'].apply(count_article_length)
    df = df[df['stemmed_count'] > MIN_ARTICLE_LENGTH]
    df = df.drop_duplicates(subset='articles_stemmed').drop('urls')

    # split into dfs for combined, and each source (to find word counts for descriptive stats)
    df_source_one = df[ df['source'] == SOURCE_ONE].copy()
    df_source_two = df[ df['source'] == SOURCE_TWO].copy()
    df_subset     = df[(df['source'] == SOURCE_ONE) | (df['source'] == SOURCE_TWO)].copy()

    # count total ngrams by source
    # this fills the dictionary passed in 'args'
    print('Counting by source and source pair...')
    df_source_one[N_GRAMS].apply(count_all, args=[SOURCE_ONE_COUNTS])
    df_source_two[N_GRAMS].apply(count_all, args=[SOURCE_TWO_COUNTS])
    df_subset[N_GRAMS].apply(count_all, args=[TOTAL_COUNTS])

    # view top ngrams
    # print(get_top_ngrams(TOTAL_COUNTS))
    # print(get_top_ngrams(SOURCE_ONE_COUNTS))
    # print(get_top_ngrams(SOURCE_TWO_COUNTS))

    # create vocabulary and index
    print('Creating vocabs...')
    create_vocab( TOTAL_COUNTS, VOCAB, VOCAB_INDEX_DICT, vocab_size=1000 )

    # create document counts
    print('Creating document "bags"')
    df_subset['bag_of_ngrams'] = df_subset[N_GRAMS].apply( bag_of_ngrams, args=[ VOCAB, VOCAB_INDEX_DICT ])

    # construct final df of this form: 
    # 
    # 'article_id', 'source', ngram_1, ngram_2, ... , ngram_p
    # ------------  --------  -------  -------  ...   ------
    #       1     ,  'Fox'  ,     0  ,     1  , ... ,     0 
    #       .
    #       . 
    #       . 
    print('Creating final matrix and saving...')
    df_final = construct_final_df(df_subset, VOCAB)
    df_final.to_csv(MATRIX_VALUES_FILE)
    print('Matrix saved.')