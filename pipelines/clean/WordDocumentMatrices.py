import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

news = pd.read_csv('../../data/newsapi_corpus_cleaned.csv').fillna('')
world_news = pd.read_csv('../../data/worldnewsapi_corpus_cleaned.csv').fillna('')
ground_news = pd.read_csv('../../data/groundnews_corpus_cleaned.csv',index_col=0).fillna('')


#Extract the metadata, we'll add it back in later
news_metadata = news.loc[:,('author','publishedAt','source','url','urlToImage')]
world_news_metadata = world_news.loc[:,('authors','country','sentiment','url')]
ground_news_metadata = ground_news.loc[:,('bias','factuality','owner','source','owner_type')]


cv = CountVectorizer(stop_words='english')
cv_2 = CountVectorizer(stop_words='english',ngram_range=(2,2))
tv = TfidfVectorizer(stop_words='english')
tv_2 = TfidfVectorizer(stop_words='english',ngram_range=(2,2))

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
news_title_l_cv = create_wdm(news['title_l'], news_metadata, cv, 3)
news_desc_l_cv = create_wdm(news['desc_l'], news_metadata, cv, 3)
news_content_l_cv = create_wdm(news['content_l'], news_metadata, cv, 3)
news_title_l_tv = create_wdm(news['title_l'], news_metadata, tv, 3)
news_desc_l_tv = create_wdm(news['desc_l'], news_metadata, tv, 3)
news_content_l_tv = create_wdm(news['content_l'], news_metadata, tv, 3)

news_title_s_cv = create_wdm(news['title_s'], news_metadata, cv, 3)
news_desc_s_cv = create_wdm(news['desc_s'], news_metadata, cv, 3)
news_content_s_cv = create_wdm(news['content_s'], news_metadata, cv, 3)
news_title_s_tv = create_wdm(news['title_s'], news_metadata, tv, 3)
news_desc_s_tv = create_wdm(news['desc_s'], news_metadata, tv, 3)
news_content_s_tv = create_wdm(news['content_s'], news_metadata, tv, 3)


#Create the WDMs for World News
world_news_title_s_cv = create_wdm(world_news['title_s'], world_news_metadata, cv, 6)
world_news_text_s_cv = create_wdm(world_news['text_s'], world_news_metadata, cv, 15)
world_news_title_s_tv = create_wdm(world_news['title_s'], world_news_metadata, tv, 6)
world_news_text_s_tv = create_wdm(world_news['text_s'], world_news_metadata, tv, 15)

world_news_title_l_cv = create_wdm(world_news['title_l'], world_news_metadata, cv, 6)
world_news_text_l_cv = create_wdm(world_news['text_l'], world_news_metadata, cv, 15)
world_news_title_l_tv = create_wdm(world_news['title_l'], world_news_metadata, tv, 6)
world_news_text_l_tv = create_wdm(world_news['text_l'], world_news_metadata, tv, 15)

# Can't create this one as it's too large XD. We'll have to shrink it somehow in the process of making it..
# world_news_text_sn2 = create_wdm(world_news['text'], world_news_metadata, cv_sn2, 12)

#Saving WDMs to csv.
news_title_s_cv.to_csv('../../data/wdms/count/newsapi/stemmed/title.csv')
news_desc_s_cv.to_csv('../../data/wdms/count/newsapi/stemmed/desc.csv')
news_content_s_cv.to_csv('../../data/wdms/count/newsapi/stemmed/content.csv')
news_title_s_tv.to_csv('../../data/wdms/tfidf/newsapi/stemmed/title.csv')
news_desc_s_tv.to_csv('../../data/wdms/tfidf/newsapi/stemmed/desc.csv')
news_content_s_tv.to_csv('../../data/wdms/tfidf/newsapi/stemmed/content.csv')

news_title_l_cv.to_csv('../../data/wdms/count/newsapi/lemmed/title.csv')
news_desc_l_cv.to_csv('../../data/wdms/count/newsapi/lemmed/desc.csv')
news_content_l_cv.to_csv('../../data/wdms/count/newsapi/lemmed/content.csv')
news_title_l_tv.to_csv('../../data/wdms/tfidf/newsapi/lemmed/title.csv')
news_desc_l_tv.to_csv('../../data/wdms/tfidf/newsapi/lemmed/desc.csv')
news_content_l_tv.to_csv('../../data/wdms/tfidf/newsapi/lemmed/content.csv')


world_news_title_s_cv.to_csv('../../data/wdms/count/worldnewsapi/stemmed/title.csv')
world_news_text_s_cv.to_csv('../../data/wdms/count/worldnewsapi/stemmed/text.csv')
world_news_title_l_cv.to_csv('../../data/wdms/count/worldnewsapi/lemmed/title.csv')
world_news_text_l_cv.to_csv('../../data/wdms/count/worldnewsapi/lemmed/text.csv')

world_news_title_s_cv.to_csv('../../data/wdms/tfidf/worldnewsapi/stemmed/title.csv')
world_news_text_s_cv.to_csv('../../data/wdms/tfidf/worldnewsapi/stemmed/text.csv')
world_news_title_l_cv.to_csv('../../data/wdms/tfidf/worldnewsapi/lemmed/title.csv')
world_news_text_l_cv.to_csv('../../data/wdms/tfidf/worldnewsapi/lemmed/title.csv')

