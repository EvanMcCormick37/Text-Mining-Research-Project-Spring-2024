import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

df = pd.read_csv('../../data/ground_news_articles_raw.csv')

sources=df['source']
source_texts=[]

whitespace = re.compile(r'\s+')

for source in sources:
    conf = ''
    text = ''
    #For each source page, get the full html as a BeautifulSoup Object
    try:
        soup = BeautifulSoup(requests.get(source,timeout=10).content,'html.parser').body
        #This is code I found online which rips out style and scripts in the page. This
        #is useful for extracting the text content.
        for script in soup(['script', 'style','[document]', 'head', 'title']):
            if script is not None:
                script.extract()
        
        #Another tactic to extract the story without getting ads and stuff. It seems
        #many news sites tag their main story. This does result in a lot of blank
        #rows, but I figure a blank row is less problematic than a row filled with
        #junk words.
        # if soup.find(id=re.compile('main|content|article|story')) is not None:
        #     text = re.sub(whitespace, ' ',soup.find(id=re.compile('main|content|article|story')).get_text())
        #     conf = 'high'
        # elif soup.find_all('article') is not None or soup.find_all('p') is not None:
        #     if soup.find_all('article') is not None:
        #         text += ' '.join([re.sub(whitespace, ' ', a.get_text()) for a in soup.find_all('article')])
        #     if soup.find_all('p') is not None:
        #         text += ' '.join([re.sub(whitespace, ' ', p.get_text()) for p in soup.find_all('p')])
        #     conf = 'med'
        # else:
        #     text = re.sub(whitespace, ' ',soup.get_text())
        #     conf = 'low'
            
        text = re.sub(whitespace, ' ',soup.get_text())
        
        source_texts+=[text]
    except:
        source_texts+=['']
        continue

df['source_text']=source_texts
df.to_csv('../../data/ground_news_articles_raw.csv')
