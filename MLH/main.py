from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from datetime import date, timedelta
from time import sleep
from pymongo import MongoClient

import requests


# Replace these placeholders with your actual MongoDB URL and database name
MONGODB_URL = 'YOUR_MONGODB_URL_HERE'
DATABASE_NAME = 'YOUR_DATABASE_NAME_HERE'

# Initialize MongoDB client and database
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
hackathons_collection = db['prev_hackathons']

# list for testing
# hackathons_collection = [] 

options = Options()
# options.add_argument("--window-size=1920x1080")
# options.add_argument("--verbose")
# options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

# getting this month and next month
current_date = date.today()
current_month = current_date.strftime("%b").upper()
next_month = date.today() + timedelta(days=30)
next_month = next_month.strftime("%b").upper()
# print("Current Month:", month)
# print(next_month)


def fetch_hacks():
    print("Fetching hacks...")
    driver.get("https://mlh.io/seasons/2024/events")
    
    EVENTS = []
    
    try:
        element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'event-wrapper'))
        )

        event_wrapper = driver.find_elements(By.CLASS_NAME, "event-wrapper")
    except:
        print("Cannot load data")

    for event in event_wrapper:
        event_name = event.find_element(By.CLASS_NAME, "event-name").text
        event_link = event.find_element(By.CLASS_NAME, "event-link").get_attribute("href")
        event_mode = event.find_element(By.CLASS_NAME, "event-hybrid-notes").text
        event_date = event.find_element(By.CLASS_NAME, "event-date").text
        
        event_details = [event_name, event_link, event_mode, event_date]
        EVENTS.append(event_details)
    
    return EVENTS
    
    
def validate_hacks():
    all_hacks = fetch_hacks()
    new_hacks = []
    
    print("Validating hacks...")
    for event in all_hacks:
        # checking if date is this month or next month
        if event[3][0:3] == current_month or event[3][0:3] == next_month:
            if event not in hackathons_collection:
                new_hacks.append(event)
    
    return new_hacks

def main():
    print("Running...")
    
    while True:
        
        try:
            new_hacks = validate_hacks()
            
            if new_hacks:
                print("New hacks found on MLH:")
                
                for hack in new_hacks:
                    print(hack)
            else:
                print("No new hacks")
                break
            
            # sending new hackathons to endpoint
            ENDPOINT_URL = 'YOUR_ENDPOINT_URL_HERE'
            try:
                response = requests.post(ENDPOINT_URL, json=new_hacks)
                response.raise_for_status()  # Raise an exception if the request fails (e.g., 4xx or 5xx status codes)
                print("Successfully sent new hackathons to the endpoint.")
            except requests.exceptions.RequestException as request_error:
                print("Error sending hackathons to the endpoint:", request_error)

            # Insert new hackathons into MongoDB
            hackathons_collection.insert_many(new_hacks)
                    
        except Exception as E:
            print("Error:", E)
            driver.quit()
            break
    
if __name__ == "__main__":
    main()

