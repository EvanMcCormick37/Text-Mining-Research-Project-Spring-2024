import requests
import pandas as pd

df1 = pd.DataFrame(columns=['title','description','content','author','publishedAt','source','url','urlToImage'])

#Changing sorting parameters to get around the free API limitations.
#There is a maximum page limit of 5, limiting the number of results seen even further than would be possible given the 100 queries/day limitation.

#Articles sorted by publish date by default
for num in range(1,6):  
    request_params = {'q':'transgender',
                      'page':f'{num}',
                      'language':'en',
                      'apiKey':'edb887b5553c43aab598452a6335ad0c'}
    response = requests.get('https://newsapi.org/v2/everything',request_params)
    
    json = response.json()
    articles = json['articles']
        
    for article in articles:
        df1.loc[len(df1.index)]=[
        article['title'],
        article['description'],
        article['content'],
        article['author'],
        article['publishedAt'],
        article['source']['id'],
        article['url'],
        article['urlToImage']
        ]
        
df2 = pd.DataFrame(columns=['title','description','content','author','publishedAt','source','url','urlToImage'])

#Same query sorted by relevancy
for num in range(1,6):  
    request_params = {'q':'transgender',
                      'page':f'{num}',
                      'sortBy':'relevancy',
                      'language':'en',
                      'apiKey':'edb887b5553c43aab598452a6335ad0c'}
    response = requests.get('https://newsapi.org/v2/everything',request_params)
    
    json = response.json()
    articles = json['articles']
        
    for article in articles:
        df2.loc[len(df2.index)]=[
        article['title'],
        article['description'],
        article['content'],
        article['author'],
        article['publishedAt'],
        article['source']['id'],
        article['url'],
        article['urlToImage']
        ]
        
df3 = pd.DataFrame(columns=['title','description','content','author','publishedAt','source','url','urlToImage'])

#Same Query sorted by popularity
for num in range(1,6):  
    request_params = {'q':'transgender',
                      'page':f'{num}',
                      'sortBy':'popularity',
                      'language':'en',
                      'apiKey':'edb887b5553c43aab598452a6335ad0c'}
    response = requests.get('https://newsapi.org/v2/everything',request_params)
    
    json = response.json()
    articles = json['articles']
        
    #I kept every piece of information attached to each article in its own column in the raw text dataframe, even if the last two ultimately proove irrelevant. 
    #Better to have extra irrelevant data than leave out something important.
    for article in articles:
        df3.loc[len(df3.index)]=[
        article['title'],
        article['description'],
        article['content'],
        article['author'],
        article['publishedAt'],
        article['source']['id'],
        article['url'],
        article['urlToImage']
        ]

df_all = pd.concat([df1,df2,df3]).drop_duplicates()
    
# df_all.to_csv('../../data/newsapi_transgender_articles_raw.csv')

