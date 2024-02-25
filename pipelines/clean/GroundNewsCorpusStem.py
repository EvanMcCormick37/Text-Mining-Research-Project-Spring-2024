import pandas as pd
import numpy as np
import re
import nltk
from nltk.stem import PorterStemmer

ps = PorterStemmer()
ground_news = pd.read_csv('../../data/groundnews_corpus_clean.csv',index_col=0).fillna('')
junk = re.compile('[^a-zA-Z\\d]')

#slice the text into words and stem each word
def stem(text):
    word_list = re.split(' ',text)
    word_list = word_list = [re.sub(junk,'',word) for word in word_list]
    word_list = [ps.stem(word) for word in word_list]
    return ' '.join(word_list)

v_stem = np.vectorize(stem)

#Add columns for stemmed version of title, summary, and source text.
ground_news.loc[:,'title_s'] = v_stem(ground_news.loc[:,'title'])
ground_news.loc[:,'summary_s'] = v_stem(ground_news.loc[:,'summary'])
ground_news.loc[:,'source_text_s'] = v_stem(ground_news.loc[:,'source_text'])

ground_news.to_csv('../../data/groundnews_corpus_cleaned.csv')