library(tidyverse)
rm(list=ls())

##################################################################################
# Storage
##################################################################################

# ADJUST PARAMS HERE
# select source_one to be the more liberal source i.e. Vox or PBS
# select source_two to be the more conservative i.e. PBS or Fox
source_one <- 'vox'
source_two <- 'pbs'
ngrams <- 3

MATRIX_FILE <- paste0('./data/', tolower(source_one), '_', tolower(source_two), '_', ngrams, '_gram_counts.csv')
SAVE_FILE_PATH <- paste0('./data/R_data/', tolower(source_one), '_', tolower(source_two), '_', ngrams, '_gram_counts.rda')

##################################################################################
# Read data
##################################################################################

df <- read_csv(MATRIX_FILE)

##################################################################################
# Transform and clean
##################################################################################

# get the vocabulary
# note: the first two columns are `article id` and 'source'
vocab <- colnames(df)[3:length(colnames(df))]

# get article source
article_source <- data.frame(news_source=df$source)
rownames(article_source) <- df$`article id`

# get the ngram counts into a sparse matrix form 
article_ngram_counts <- map(df[3:length(colnames(df))], Matrix::Matrix, sparse = T) %>% 
  reduce(cbind2)
rownames(article_ngram_counts) <- df$`article id`
colnames(article_ngram_counts) <- vocab

# sanity checks

# article_ngram_counts[1:3, 1:5]
# article_source[1:3,]
# rownames(article_source)[1:3]

##################################################################################
# Save
##################################################################################

save(article_ngram_counts, article_source, vocab, file=SAVE_FILE_PATH)

