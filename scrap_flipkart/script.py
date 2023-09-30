import pandas as pd
import requests 
from bs4 import BeautifulSoup
Product_name=[]
Prices=[]
Description=[]
Reviews=[]
for i in range(2,12):
  url="https://www.flipkart.com/search?q=mobile%20under%2050%2C000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"+str(i)
  r=requests.get(url)
  soup=BeautifulSoup(r.text,"lxml")
  soup=BeautifulSoup(r.text,"lxml")
  box=soup.find("div",class_="_1YokD2 _3Mn1Gg")
  names=box.find_all("div",class_="_4rR01T")
  for i in names:
    name=i.text
    Product_name.append(name)
  prices=box.find_all("div",class_="_30jeq3 _1_WHN1")
  for i in prices:
    name=i.text
    Prices.append(name)
  desc=box.find_all("ul",class_="_1xgFaf")
  for i in desc:
    name=i.text
    Description.append(name)
  reviews=box.find_all("div",class_="_3LWZlK")
  for i in reviews:
    name=i.text
    Reviews.append(i)
  df=pd.DataFrame({"Product Name":Product_name,"Prices":Prices,"Description":Description,"Reviews":Reviews})
  print(df)