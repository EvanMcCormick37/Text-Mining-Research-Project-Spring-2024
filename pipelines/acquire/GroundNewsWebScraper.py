from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

df = pd.DataFrame(columns = ['title','summary','bias','factuality','owner','source'])
print('running!')

#Get into the topic page on Ground News for the topic of transgender.
#There is a button on Ground News to expand the article selection. I don't know how to click it within a python
#url request and clicking it does nothing to change the URL, so instead I populated the page with as many articles
#as I was allowed and then copied the resulting html into a local .txt file. I'm using this html as my basis here.
file = open('../../data/ground_news_transgender_interest.html',encoding="utf8",mode='r')
#main_page = requests.get('https://ground.news/interest/transgender')
content = file.read()
file.close()
soup = BeautifulSoup(content,'lxml').body

articles = []
#Make a list of article links by looking for all links in the body which contain
#/article/. These all link to article pages on ground news.
for article in soup.find_all(href=re.compile('article')):
    articles.append('https://ground.news'+article.get('href'))
    
i=1
#keep a running tally of articles so i can stay sane while it's working

for article in articles:
    print(str(i)+'/97')
    i+=1
    #Go to the article page on ground news. This is a list of stories from different sources
    #about the same event, along with information about the sources of each story.
    article_page = requests.get(article)
    article_soup = BeautifulSoup(article_page.content,'html.parser').body
    
    stories = article_soup.find_all(id="article-summary")
    
    #For each story, get the source-bias, factuality rating, summary, and owner of the company.
    #Then follow the link to the original story and grab the original story's text.
    for story in stories:
        
        title = story.find('h4').get_text() if story.find('h4') is not None else '';
        summary = story.find('p').get_text() if story.find('p') is not None else '';
        
        #Bias, Factuality, and Owner buttons may not be present. Return an empty string if
        #BeautifulSoup can't find them.
        bias = story.find(id=re.compile('article-source-bias')).get_text() if story.find(id=re.compile('article-source-bias')) is not None else ''
        
        factuality = story.find(id=re.compile('article-source-factuality')).get_text() if story.find(id=re.compile('article-source-factuality')) is not None else ''
        
        owner = story.find(id=re.compile('article-source-owner')).get_text() if story.find(id=re.compile('article-source-owner')) is not None else ''
        
        if story.find('a') is not None:
            source_url = story.find('a').get('href')
            # I think trying to add the source text might be resulting in memory errors in this environment, I can't get the code to complete.
            
            # source_page = requests.get(source_url)
            # source_soup = BeautifulSoup(source_page.content,'html.parser')
            
            # #get rid of scripts and styles in the source page
            # for script in soup(["script", "style"]):
            #     script.extract()
            
            # #get the raw text. Not formatting any more here because these pages will
            # #vary wildly in their structure due to being from different websites.
            # source_text = source_soup.get_text()
        else:
            source_url = ''
        
        #Add all of the values relating to this story to the dataframe.
        df.loc[len(df.index)] = [(title if title is not None else ''),
                                 (summary if summary is not None else ''),
                                 (bias if bias is not None else ''),
                                 (factuality if factuality is not None else ''),
                                 (owner if owner is not None else ''),
                                 (source_url if source_url is not None else '')]
df = df.drop_duplicates()
df[['owner_type','owner']]=df['owner'].str.split(': ', n=1, expand=True)
#df.to_csv('../../data/ground_news_articles_raw.csv',index=False)