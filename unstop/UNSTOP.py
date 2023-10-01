from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import requests


MONGODB_URL = 'YOUR_MONGODB_URL_HERE'
DATABASE_NAME = 'YOUR_DATABASE_NAME_HERE'

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
hackathons_collection = db['prev_hackathons']
# hackathons_collection = []
path = r"E:\dd\chromedriver-win64\chromedriver-win64\chromedriver.exe"  #set path for web driver
options = Options()
# options.add_argument("--window-size=1920x1080")
# options.add_argument("--verbose")
options.add_argument("--headless=new")            #implementing headless to work without extra window
browser = webdriver.Chrome(executable_path=path,options=options)

browser.get("https://unstop.com/hackathons")


def extract_name(list1,list2):   #substrating the string containing all the details from the string containing place
    res = [ ele for ele in list1 ]
    for a in list2:
        if a in list1:
            res.remove(a)          #name+place - place = name
    return res


def find_hacks():                   # function to extract hackathons from unstop

    hackathons = []

    # try:

    hack_xpath = "//div[@class='content']"

    hackathons = []

    hack_list = browser.find_elements(By.XPATH,hack_xpath)
    # for p in hack_list:
    #     print(p.text)
    for hack in hack_list:
        hack.click()
        sleep(1)

        try:                                    #dealing with the login pop up
            sleep(10)
            login_up = browser.find_element(By.XPATH,"//div[@class='bg_box login_modal']")
            close = browser.find_element(By.XPATH,"//em[@class ='material-icons close_icon gtm_modal_close_btn ng-star-inserted']")
            close.click()
            sleep(1)

        except:
            pass

        try:                                    # dealing with the accept cookies pop up
            sleep(1)
            cookies = browser.find_element_by_xpath("//div[@class='box_right_bottom site-update ng-star-inserted']")
            ok_but = browser.find_element_by_xpath("//div[@class='desk']")
            ok_but.click()
            sleep(1)
        except:
            pass
        isopen = browser.find_element(By.XPATH,"//div[@class='register_sect ng-star-inserted']")

        for x in isopen.text.split():

            if x == "Register":                     #checking if the registration of certain hackathon is still there or closed
                reg_open = True
                break
            else:
                reg_open = False

        if reg_open == True:
            hack_overall = browser.find_element(By.CSS_SELECTOR,"div[class='cptn 456']>h1")         #scraping name and place
            hack_place = browser.find_element(By.CSS_SELECTOR,"div[class='cptn 456']>h1>span")      #scraping place
            hack_mode = browser.find_element(By.CSS_SELECTOR,"div[class='items ml-10 single-wrap']")#scraping mode of hackathon
            hack_overall_list = hack_overall.text.split()
            hack_name_list = hack_place.text.split()

            hack_name_l = extract_name(hack_overall_list,hack_name_list)

            hack_name = ""

            for x in hack_name_l:
                hack_name += x+" "              #convertign list containing hackathon name into string

            hack_link = browser.find_element(By.XPATH,"//a[@class='register_btn cursor waves-effect ng-star-inserted']").get_attribute("href")  #scraping link of hackthon registration

            details_list = isopen.text.split()
            price = details_list[0]                         #scraping price of entry or hackathon

            hackathons.append([hack_name,hack_place.text,hack_mode.text,hack_link,price])


        else:
            continue
    return hackathons


def validate_hacks():    #filtering the new hackathons
    all_hacks = find_hacks()
    new_hacks = []

    print("Validating hacks...")
    for event in all_hacks:


        if event not in hackathons_collection:
            new_hacks.append(event)
    return new_hacks


def main():             #main program
    print("Running...")

    while True:

        try:
            new_hacks = validate_hacks()
            # print(new_hacks)

            if new_hacks:
                print("New hacks found on unpost:")

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
            browser.quit()
            break

if __name__ == "__main__":
    main()





