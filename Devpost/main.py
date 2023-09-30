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
MONGODB_URL = 'YOUR MONGODB URL'
DATABASE_NAME = 'YOUR DATABASE NAME'

# Initialize MongoDB client and database
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
hackathons_collection = db['prev_hackathons']


options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


# getting this month and next month
current_date = date.today()
current_month = current_date.strftime("%b").upper()
next_month = date.today() + timedelta(days=30)
next_month = next_month.strftime("%b").upper()
# print("Current Month:", current_month)
# print(next_month)

LINKS= []
TITLES=[]
MODES=[]
DATES=[]
EVENTS=[]

def fetch_hacks():

    print("Fetching hacks...")
    driver.get("https://devpost.com/hackathons")

# For Scrolling
    for x in range(0, 10):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        sleep(1)
        driver.execute_script("window.scrollBy(0,-300)")



    try:

        elements = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'container')))

        # hackathon_box = driver.find_elements(By.CLASS_NAME, "hackathon-tile clearfix open mb-5")
        main_content = driver.find_elements(By.CLASS_NAME, 'main-content')
        # side_content = driver.find_elements(By.CLASS_NAME, 'info')

        hackathons_container = driver.find_elements(By.CLASS_NAME,'hackathons-container')


    except:
        print("Cannot load data")


    def removeduplicate(data):
        countdict = {}
        for element in data:
            if element in countdict.keys():
                countdict[element] += 1
            else:
                countdict[element] = 1
        data.clear()
        for key in countdict.keys():
            data.append(key)

    for box in hackathons_container:
        links = box.find_elements(By.TAG_NAME, 'a')

        for link in links:
            LINKS.append(link.get_attribute('href'))



    for hackathon in main_content:
        title = hackathon.find_element(By.TAG_NAME, 'h3').text
        TITLES.append(title)


        mode = hackathon.find_element(By.CLASS_NAME,'info').text
        MODES.append(mode)


        date = hackathon.find_element(By.CLASS_NAME, 'submission-period').text
        DATES.append(date)

    removeduplicate(LINKS)


    for i in range( 0, len(LINKS)):

        event_details = [ TITLES[i], LINKS[i], MODES[i], DATES[i] ]
        EVENTS.append(event_details)



    print(len(DATES))
    return EVENTS






def validate_hacks():
    all_hacks = fetch_hacks()
    new_hacks = []

    print("Validating hacks...")
    for event in all_hacks:
        # checking if date is this month or next month

        hack_month = event[3][0:3].upper()
        print(hack_month)
        if hack_month == current_month or hack_month == next_month:
            if event not in hackathons_collection:
                new_hacks.append(event)


    return new_hacks


def main():



    print("Running...")

    while True:

        try:
            new_hacks = validate_hacks()

            if new_hacks:
                print("New hacks found on Devpost:")

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




