import requests
import pandas as pd

df = pd.DataFrame(columns=['title','text','authors','country','sentiment','url'])
#Going to extract a bunch of news articles from the past couple of months from this API as well.
url = 'https://api.worldnewsapi.com/search-news'

for o in range(0,3001,100):
    request_params = {'text':'transgender',
                      'number':'100',
                      'offset':f'{o}',
                      'earliest-publish-date':'2023-09-01',
                      'sort':'publish-time',
                      'language':'en',
                      'api-key':'968a873ef4a14e2fb2acc6a0107ccbea'}
    print(f'requesting articles {o+1}-{o+101}!')
    
    resp = requests.get(url,request_params)
    json = resp.json()
    articles =json['news']
    
    for article in articles:
        df.loc[len(df.index)]=[
        article['title'],
        article['text'],
        article['authors'][0] if len(article['authors'])>0 else '',
        article['source_country'],
        article['sentiment'],
        article['url']
        ]
        
df = df.drop_duplicates()
df.to_csv('../../data/worldnewsapi_corpus_raw.csv',mode='a')