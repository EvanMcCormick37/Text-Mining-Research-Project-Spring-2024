import pandas as pd
import numpy as np
import re
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Here I'm cleaning the Ground News articles to form a cleaned corpus.
#My main task here is using the Ground News summary for each article to remove 
#superfluous words from the article's source text.
#My plan is:
#1. Split the source text and summary into word lists and lemmatize them (while maintaining duplicates, stop words, and word order)
#2. Remove all stop words from the summary word list
#3. Find the first and last indices of words in the source text which match a word in the summary word list
#4. Throw out all source text words which fall outside of those indices.
#This should hopefully remove all of the ads which were displayed before and after the main story, while keeping the bulk of the main
#story for each source text article.
df = pd.read_csv('../../data/groundnews_corpus_raw.csv',index_col=0).fillna('')
wnl = WordNetLemmatizer()
junk = re.compile('[^a-zA-Z\\d]')
stop_words = set(stopwords.words('english'))

#I tried vectorizing separate functions for each step of this process, but pandas
#and numpy don't like the intermediate state of having three columns of the dataframe
#be columns with a list in each cell. So instead I'm combining all steps into one function which
#will return the cleaned title, summary, and source text. Then I'll vectorize it and run it across the
#data frame.

#Helper function for lemmatizing a text and returning the lemmatized word list
def lemmatize(text):
    word_list = re.split(junk,text)
    word_list = [re.sub(junk,'',word) for word in word_list]
    word_list = [wnl.lemmatize(word) for word in word_list]
    return word_list

#I tried filtering on the title as well as the summary, and filtering on the title gave me much better results.
def clean_source_text(t,s,s_t):
    #Step 1
    t=lemmatize(t)
    s=lemmatize(s)
    s_t=lemmatize(s_t)

    #Step 2
    t = [w for w in t if not w.lower() in stop_words]
    
    #Step 3
    t_in_s_t = [w in t for w in s_t]
    # s_in_s_t = [w in s for w in s_t]
    
    title_matching_indices = [i for i,x in enumerate(t_in_s_t) if x]
    # summary_matching_indices = [i for i,x in enumerate(s_in_s_t) if x]
    
    title = ' '.join(t)
    summary = ' '.join(s)
    #Step 4
    if len(title_matching_indices)>1:
        source_text = s_t[title_matching_indices[0]:title_matching_indices[-1]]
    # elif len(summary_matching_indices)>1:
    #     source_text = s_t[summary_matching_indices[0]:summary_matching_indices[-1]]
    else:
        source_text = ['']
    print(len(s_t)-len(source_text))
    
    source_text = ' '.join(source_text)
    
    return title, summary, source_text

for i in range(len(df)):
    df.loc[i,'title'],df.loc[i,'summary'],df.loc[i,'source_text'] = clean_source_text(
        df.loc[i,'title'],df.loc[i,'summary'],df.loc[i,'source_text'])

df.to_csv('../../data/groundnews_corpus_cleaned.csv')