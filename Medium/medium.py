from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def getLinks():
    topic = str(input("Enter topic:"))
    num = int(input("Enter number of articles:"))
    url = f"https://medium.com/tag/{topic}/archive"
    links = []
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all('article')
    for article in articles[:num]:
        anchor = article.find_all('a')[2]
        link = anchor.get('href').split("?")[0]
        links.append(link)
        
    return links

def scrape_article(link):
    text = ""
    url = f"https://medium.com{link}"
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    paras = soup.find_all("p",class_="pw-post-body-paragraph")
    for para in paras:
        text+= str(para.text)
    return text



if __name__=="__main__":
    links = getLinks()
    for link in links:
        text = scrape_article(link)
    with open("Data.txt", "w", encoding="utf-8") as file:
        file.write(text)