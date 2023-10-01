from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

import requests

# Replace these placeholders with your actual MongoDB URL and database name
# MONGODB_URL = 'YOUR MONGODB URL'
# DATABASE_NAME = 'YOUR DATABASE NAME'

# Initialize MongoDB client and database
# client = MongoClient(MONGODB_URL)
# db = client[DATABASE_NAME]
# song_link = db['prev_hackathons']


options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)




def fetch_song():


    driver.get("https://wynk.in/music/search")

    try:

        music_input = input("Enter the song name: ")
        driver.implicitly_wait(10)




        page = driver.find_elements(By.XPATH, '//*[@id="__next"]/header/section')
        # print(page)




    except:
        print("Cannot load data")
    for item in page:
        search = item.find_element(By.TAG_NAME,'input')
        # print(search)
        search.send_keys(music_input, Keys.ENTER)
        break

    search_list = driver.find_elements(By.CLASS_NAME, 'zapSearch_zapSearchList__TvGT1')
    # print(search_list)

    for item in search_list:
        song = item.find_element(By.TAG_NAME,'a').get_attribute("href")
        # print(song)
        break


    song_details = [ music_input , song]

    return song_details
    # print(song_details)


def main():


    print("Running...")

    while True:

            song_details = fetch_song()





            # sending new song to endpoint
            ENDPOINT_URL = 'YOUR_ENDPOINT_URL_HERE'
            try:
                response = requests.post(ENDPOINT_URL, json=song_details)
                response.raise_for_status()  # Raise an exception if the request fails (e.g., 4xx or 5xx status codes)
                print("Successfully sent latest news to the endpoint.")
            except requests.exceptions.RequestException as request_error:
                print("Error sending news to the endpoint:", request_error)

             # Insert song details into MongoDB
            # song_link.insert_many(song_details)
            print(song_details)
            break




if __name__ == "__main__":
    main()

