import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/world-population/population-by-country"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find("table", {'id': 'example2'}).find('tbody').find_all('tr')
countries_list = []

for row in rows:
    dic = {}
    dic['country'] = row.find_all('td')[1].text
    dic["population"] = row.find_all('td')[2].text.replace(',', '')

    countries_list.append(dic)

df = pd.DataFrame(countries_list)
df.to_excel("countries_data.xlsx", index=False)
df.to_csv("countries_data.csv", index=False)