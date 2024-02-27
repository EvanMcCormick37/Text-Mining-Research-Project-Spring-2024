import pandas as pd
import numpy as np
import re
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

news = pd.read_csv('../../data/newsapi_corpus_raw.csv',index_col=0)
world_news = pd.read_csv('../../data/worldnewsapi_corpus_raw.csv',index_col=0)

wnl = WordNetLemmatizer()
ps = PorterStemmer()
junk = re.compile('[^a-zA-Z\\d]')

#Split the text along white-space and remove junk, then lemmatize
def lemmatize(text):
    word_list = re.split(' ',text)
    word_list = [re.sub(junk,'',word) for word in word_list]
    word_list = [wnl.lemmatize(word) for word in word_list]
    return ' '.join(word_list)
v_lemm = np.vectorize(lemmatize)

#Same process but with the PorterStemmer rather than the WordNetLemmatizer
def stem(text):
    word_list = re.split(' ',text)
    word_list = word_list = [re.sub(junk,'',word) for word in word_list]
    word_list = [ps.stem(word) for word in word_list]
    return ' '.join(word_list)
v_stem = np.vectorize(stem)
#Fill nan values
news = news.fillna('')
world_news = world_news.fillna('')

# I did this already, now commenting it out for ease of use for stemming.

#Add stemmed and lemmed versions of News as columns
news.loc[:,'title_s']=v_stem(news.loc[:,'title'])
news.loc[:,'desc_s']=v_stem(news.loc[:,'description'])
news.loc[:,'content_s']=v_stem(news.loc[:,'content'])
news.loc[:,'title_l']=v_lemm(news.loc[:,'title'])
news.loc[:,'desc_l']=v_lemm(news.loc[:,'description'])
news.loc[:,'content_l']=v_lemm(news.loc[:,'content'])

#Do the same for world_news
world_news.loc[:,'text_s']=v_stem(world_news.loc[:,'text'])
world_news.loc[:,'text_l']=v_lemm(world_news.loc[:,'text'])
world_news.loc[:,'title_s']=v_stem(world_news.loc[:,'title'])
world_news.loc[:,'title_l']=v_lemm(world_news.loc[:,'title'])

news.to_csv('../../data/newsapi_corpus_cleaned.csv',index=0)
world_news.to_csv('../../data/worldnewsapi_corpus_cleaned.csv',index=0)