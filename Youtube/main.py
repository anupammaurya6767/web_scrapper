from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def results(channelname):
    Videos=[]
    viewsandlikes=[]
    totalviews=[]
    likes=[]
    driver=webdriver.Chrome()
    driver.get('https://www.youtube.com/@'+str(channelname)+'/videos')
    content=driver.page_source.encode('utf-8').strip()
    soup=BeautifulSoup(content,'lxml')
    titles=soup.findAll('a',id='video-title-link')
    views=soup.findAll('span',class_="inline-metadata-item style-scope ytd-video-meta-block")
    for title in titles:
        Videos.append(title.text.split("|")[0])
    for view in views:
        viewsandlikes.append(view.text)
    for i in range(len(viewsandlikes)):
        if i%2==0:
            totalviews.append(viewsandlikes[i])
        else:
            likes.append(viewsandlikes[i])
    df=pd.DataFrame({"Videos Title":Videos,"Views":totalviews,"Likes":likes})
    df.to_csv(str(channelname)+"_info.csv",index=False)
    return "CSV file created!!"

print(results(input("Please enter a Youtube Channel: ")))