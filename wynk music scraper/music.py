from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import requests


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

    # time.sleep(10)
    song_details = [ music_input , song]

    return song_details
    # print(song_details)



def main():

    #EXAMPLE
    song_details=fetch_song()
    print(song_details)


if __name__ == "__main__":
    main()

