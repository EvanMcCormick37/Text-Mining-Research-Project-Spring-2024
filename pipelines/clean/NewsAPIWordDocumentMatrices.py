import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

news = pd.read_csv('../../data/newsapi_corpus_lemmatized.csv').fillna('')
world_news = pd.read_csv('../../data/worldnewsapi_corpus_lemmatized.csv').fillna('')

#Extract the metadata, we'll add it back in later
news_metadata = news.loc[:,('author','publishedAt','source','url','urlToImage')]
world_news_metadata = world_news.loc[:,('authors','country','sentiment','url')]


cv_s = CountVectorizer(stop_words='english')
cv_sn2 = CountVectorizer(stop_words='english',ngram_range=(2,2))

#This function transforms the text into a word-document matrix containing all words
#which occur at least twice (this is to cut down on size, under the assumption that the words which occur
#once are more trouble than they're worth), and sorts the matrix based on frequency.
def create_wdm(series,metadata,cv,n):
    wdm = cv.fit_transform(series)
    wdm_df = pd.DataFrame(data=wdm.toarray(),columns=cv.get_feature_names_out())
    wdm_df.loc['sum'] = wdm_df.sum()
    #Filter for words with a minimum frequency. Cuts down on junk and size
    wdm_df = wdm_df.loc[:,wdm_df.loc['sum']>n]
    #filter for strings greater than a certain length. Cuts out some silliness.
    wdm_df = wdm_df.filter(regex=r'^[a-zA-Z]{3,}$')
    wdm_df = wdm_df.sort_values(by='sum',axis=1,ascending=False)
    wdm_df = pd.concat([metadata,wdm_df],axis=1,join='inner')
    return wdm_df

#Create the WDMs for News. Altering min number of occurances to keep the size of larger WDMs in check.
news_title_s = create_wdm(news['title'], news_metadata, cv_s, 3)
news_desc_s = create_wdm(news['description'], news_metadata, cv_s, 3)
news_content_s = create_wdm(news['content'], news_metadata, cv_s, 3)
news_title_sn2 = create_wdm(news['title'], news_metadata, cv_sn2, 1)
news_desc_sn2 = create_wdm(news['description'], news_metadata, cv_sn2, 1)
news_content_sn2 = create_wdm(news['content'], news_metadata, cv_sn2, 1)

#Create the WDMs for World News
world_news_title_s = create_wdm(world_news['title'], world_news_metadata, cv_s, 6)
world_news_text_s = create_wdm(world_news['text'], world_news_metadata, cv_s, 15)
world_news_title_sn2 = create_wdm(world_news['title'], world_news_metadata, cv_sn2, 1)
# Can't create this one as it's too large XD. We'll have to shrink it somehow in the process of making it..
# world_news_text_sn2 = create_wdm(world_news['text'], world_news_metadata, cv_sn2, 12)

#Saving WDMs to csv.
news_title_s.to_csv('../../data/wdms/newsapi/title_sn1.csv')
news_desc_s.to_csv('../../data/wdms/newsapi/desc_sn1.csv')
news_content_s.to_csv('../../data/wdms/newsapi/content_sn1.csv')
news_title_sn2.to_csv('../../data/wdms/newsapi/title_sn2.csv')
news_desc_sn2.to_csv('../../data/wdms/newsapi/desc_sn2.csv')
news_content_sn2.to_csv('../../data/wdms/newsapi/content_sn2.csv')

world_news_title_s.to_csv('../../data/wdms/worldnewsapi/title_sn1.csv')
world_news_text_s.to_csv('../../data/wdms/worldnewsapi/text_sn1.csv')
world_news_title_sn2.to_csv('../../data/wdms/worldnewsapi/title_sn2.csv')

