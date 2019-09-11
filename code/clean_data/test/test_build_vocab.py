import pandas as pd 
from collections import defaultdict
import os, sys

###########################################################################
# Storage
###########################################################################

# path info 

BASE_DIR = '/Users/stevelee/Dropbox/CourseWork/Fall2019/DataScience/project/'
CLEANING_DIR = os.path.join(BASE_DIR, 'code', 'clean_data')

sys.path.append(CLEANING_DIR)
from build_vocab import count_all, create_vocab, bag_of_ngrams
from rawtxt_to_ngrams import only_alphas, ngrams, stem

###########################################################################
# Test Inputs
###########################################################################

sentence = 'this is my test sentence56'
vocab = []
total_counts = defaultdict(int)
index_dict = defaultdict(int)
bigram = ngrams(only_alphas(sentence), 2)   # get 2gram string
count_all(bigram, total_counts)                   # fill total counts dict
create_vocab(total_counts, vocab, index_dict, cutoff_ct=0)
bag_of_2grams = bag_of_ngrams(bigram, vocab, index_dict)  

print(bag_of_2grams)    # OUTPUT: 1.1.1.1
print(vocab)            # OUTPUT: ['is my', 'my test', 'test sentence', 'this is']