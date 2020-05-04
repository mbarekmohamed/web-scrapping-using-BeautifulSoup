
# Web Scraping using Beautifulsoup

### Importing the packages

import bs4 as bs
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib.parse import urljoin

# Extracting all the the URLs from pages 

relative_urls=[]
for i in range (1,16):
    url='https://www.tunisienumerique.com/actualite-tunisie/tunisie/page'+str(i)+'/'
    print('scrapping page num ',i)
    response=requests.get(url)
    response.status_code

    html=response.content

    soup=BeautifulSoup(html,'html.parser')

    #Creating links and fetching articles
    links = []


    x=soup.find_all('li',class_="infinite-post")


    aa = BeautifulSoup(str(x), "html.parser")

    links = aa.find_all('a')

    relative_url = [link.get('href') for link in links]
    for url in relative_url:
        relative_urls.append(url)
    


# Extracting all the text from the URLs

articles = []
titles =  []
types=[]
for link in relative_urls :
        result = requests.get(link)
        text=result.text
        soup = BeautifulSoup(text,'html.parser')
        
        ar = soup.find_all('div', id="content-main",class_="left relative")
        art = BeautifulSoup(str(ar), "html.parser")
        article = art.find_all('p')
        article_txt = [t.text for t in article]
        articles.append(article_txt)
        
        title = soup.find_all('h1', class_='post-title entry-title left')
        title_txt = [t.text for t in title]
        titles.append(title_txt)
        
        ty=soup.find_all('span', class_="post-head-cat")  
        type_txt = [t.text for t in ty]
        types.append(type_txt)

titles_str=["".join(text) for text in titles]
articles_str=["".join(text) for text in articles]
type_str=["".join(text) for text in types]

# creating csv file

df = pd.DataFrame(list(zip(relative_urls, titles_str , articles_str,type_str)), 
                columns =['link','titles', 'article','type'])
df["type"].replace(to_replace='\xa0',value=np.nan,inplace=True)
df.to_csv('tunisie_numerique.csv',index=False)


