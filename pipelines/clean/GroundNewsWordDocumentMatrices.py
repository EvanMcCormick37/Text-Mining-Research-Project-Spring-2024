import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


cv = CountVectorizer()
cv_s = CountVectorizer(stop_words='english')
cv_n2 = CountVectorizer(ngram_range=(2,2))
cv_sn2 = CountVectorizer(stop_words='english',ngram_range=(2,2))

#This function transforms the text into a word-document matrix containing all words
#which occur at least twice (this is to cut down on size, under the assumption that the words which occur
#once are more trouble than they're worth), and sorts the matrix based on frequency.
def create_wdm(series,cv):
    wdm = cv.fit_transform(series)
    wdm_df = pd.DataFrame(data=wdm.toarray(),columns=cv.get_feature_names_out())
    wdm_df.loc['sum'] = wdm_df.sum()
    wdm_df = wdm_df.loc[:,wdm_df.loc['sum']>5]
    wdm_df = wdm_df.sort_values(by='sum',axis=1,ascending=False)
    wdm_df = pd.concat([metadata,wdm_df],axis=1,join='inner')
    return wdm_df

#Create the simple word-document matrices
wdm_title = create_wdm(df['title'],cv)
wdm_summary = create_wdm(df['summary'], cv)
wdm_source_text = create_wdm(df['source_text'],cv)

#Create the word-document matrices with stopwords removed
wdm_title_s = create_wdm(df['title'],cv_s)
wdm_summary_s = create_wdm(df['summary'], cv_s)
wdm_source_text_s = create_wdm(df['source_text'],cv_s)

#Create the n-gram word-document matrices
wdm_title_n2 = create_wdm(df['title'],cv_n2)
wdm_summary_n2 = create_wdm(df['summary'], cv_n2)
wdm_source_text_n2 = create_wdm(df['source_text'],cv_n2)

#Create the n-gram word-document matrices no stopwords
wdm_title_sn2 = create_wdm(df['title'],cv_sn2)
wdm_summary_sn2 = create_wdm(df['summary'], cv_sn2)
wdm_source_text_sn2 = create_wdm(df['source_text'],cv_sn2)

#I'm going to put the 2-grams and 1-grams no stopwords into csv files. One for title, summary, and source text.
wdm_title_s.to_csv('../../data/wdms/groundnews/title_sn1.csv')
wdm_summary_s.to_csv('../../data/wdms/groundnews/summary_sn1.csv')
wdm_source_text_s.to_csv('../../data/wdms/groundnews/source_text_sn1.csv')
wdm_title_sn2.to_csv('../../data/wdms/groundnews/title_sn2.csv')
wdm_summary_sn2.to_csv('../../data/wdms/groundnews/summary_sn2.csv')
wdm_source_text_sn2.to_csv('../../data/wdms/groundnews/source_text_sn2.csv')