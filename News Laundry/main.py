from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
from datetime import date, timedelta
from time import sleep
import requests

# Replace these placeholders with your actual MongoDB URL and database name
# MONGODB_URL = 'YOUR MONGODB URL'
# DATABASE_NAME = 'YOUR DATABASE NAME'

# Initialize MongoDB client and database
# client = MongoClient(MONGODB_URL)
# db = client[DATABASE_NAME]
# news_collection = db['prev_hackathons']


options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)




NEWS=[]
news_collection=[]
def fetch_news():

    print("Fetching news...")
    driver.get("https://www.newslaundry.com/")

    try:

        elements = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'container')))


        boxes = driver.find_elements(By.CLASS_NAME, '_31QO6')

        # side_content = driver.find_elements(By.CLASS_NAME, 'info')
        # hackathons_container = driver.find_elements(By.CLASS_NAME,'hackathons-container')


    except:
        print("Cannot load data")

    for box in boxes:
        head_line = box.find_element(By.TAG_NAME,'h2').text
        # print(head_line)

        link = box.find_element(By.TAG_NAME,'a').get_attribute("href")
        # print(link)

        img = box.find_element(By.TAG_NAME,'img').get_attribute("src")
        # print(img)

        date = box.find_element(By.TAG_NAME,'time').text
        # print(date)


        news_details = [img, head_line, link, date]
        NEWS.append(news_details)

    # print(NEWS)
    return NEWS






def validate_hacks():
    all_news = fetch_news()
    new_news = []

    print("Validating news...")
    for news in all_news:
        if news not in news_collection:
            new_news.append(news)

    # print(new_news)
    return new_news


def main():



    print("Running...")

    while True:

        try:
            new_news = validate_hacks()
        #
            if new_news:
                print("Latest news found on News Laundry: ")
        #
                for news in new_news:
                    print(news)

            else:
                print("No new news")
                break




            # sending new hackathons to endpoint
            ENDPOINT_URL = 'YOUR_ENDPOINT_URL_HERE'
            try:
                response = requests.post(ENDPOINT_URL, json=new_news)
                response.raise_for_status()  # Raise an exception if the request fails (e.g., 4xx or 5xx status codes)
                print("Successfully sent latest news to the endpoint.")
            except requests.exceptions.RequestException as request_error:
                print("Error sending news to the endpoint:", request_error)

             # Insert new hackathons into MongoDB
            # news_collection.insert_many(new_news)
            break

        except Exception as E:
            print("Error:", E)
            driver.quit()
            break


if __name__ == "__main__":
    main()
