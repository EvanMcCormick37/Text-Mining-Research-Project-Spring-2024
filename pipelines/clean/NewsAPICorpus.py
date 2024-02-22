import pandas as pd
import numpy as np
import re
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

news = pd.read_csv('../../data/newsapi_corpus_raw.csv',index_col=0)
world_news = pd.read_csv('../../data/worldnewsapi_corpus_raw.csv',index_col=0)

wnl = WordNetLemmatizer()
junk = re.compile('[^a-zA-Z\\d]')

#Split the text along white-space and hyphens
def lemmatize(text):
    word_list = re.split(' ',text)
    word_list = [re.sub(junk,'',word) for word in word_list]
    word_list = [wnl.lemmatize(word) for word in word_list]
    return ' '.join(word_list)

#Fill nan values
news = news.fillna('')
world_news = world_news.fillna('')

for i in range(len(news)):
    #Lemmatize each text element of each news story.
    news.iloc[i,0]=lemmatize(news.iloc[i,0])
    news.iloc[i,1]=lemmatize(news.iloc[i,1])
    news.iloc[i,2]=lemmatize(news.iloc[i,2])

for i in range(len(world_news)):
    world_news.iloc[i,0] = lemmatize(world_news.iloc[i,0])
    world_news.iloc[i,1] = lemmatize(world_news.iloc[i,1])


news.to_csv('../../data/newsapi_corpus_lemmatized.csv',index=0)
world_news.to_csv('../../data/worldnewsapi_corpus_lemmatized.csv',index=0)