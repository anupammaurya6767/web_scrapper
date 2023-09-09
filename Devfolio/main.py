import requests
import lxml.html
import time
import json
from pymongo import MongoClient

# Replace these placeholders with your actual MongoDB URL and database name
MONGODB_URL = 'YOUR_MONGODB_URL_HERE'
DATABASE_NAME = 'YOUR_DATABASE_NAME_HERE'

# Initialize MongoDB client and database
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
hackathons_collection = db['prev_hackathons']

def fetch_hackathons():
    url = 'https://devfolio.co/hackathons'
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)

    div_elements = doc.xpath(
        '//div[@class="sc-iWajrY sc-bKhNmF hackathons__StyledGrid-sc-fa04e7f9-0  bhEyGM GLpDs"]//div[@class="sc-egNfGp yTbeG CompactHackathonCard__StyledCard-sc-4a10fa2a-0 ihpCnk"]')

    hackathons = []

    for div_element in div_elements:
        title_element = div_element.find(
            './/a[@class="Link__LinkBase-sc-af40de1d-0 lkflLS"]//h3[@class="sc-tQuYZ kHbpBI"]')
        title = title_element.text_content() if title_element is not None else ""

        link_element = div_element.find('.//a[@class="PillButton-sc-7655a019-0 kTVrbf"]')
        link = link_element.get('href') if link_element is not None else ""

        mode_element = div_element.find(
            './/div[@class="sc-iWajrY deNxdR"]//p[@class="sc-tQuYZ EdbiX"]')
        mode = mode_element.text_content() if mode_element is not None else ""

        starts_element = div_element.find(
            './/div[@class="sc-iWajrY sc-jKDlA-D  fIIKMx"]')
        starts_fill = starts_element.text_content() if mode_element is not None else ""
        starts = starts_fill[-8:]
        if (starts[-5:] != "Ended"):
            hackathon_info = {
                "title": title.strip(),
                "link": link.strip(),
                "mode": mode.strip(),
                "Date": starts.strip()
            }

            hackathons.append(hackathon_info)

    return hackathons

def main():
    print("Running...")

    while True:
        try:
            current_hackathons = fetch_hackathons()

            # Check for new hackathons
            new_hackathons = [hackathon for hackathon in current_hackathons if not hackathons_collection.find_one(hackathon)]

            if new_hackathons:
                print("New hackathons found:")
                for hackathon in new_hackathons:
                    pass
                print(new_hackathons)
                # Replace this placeholder with your actual endpoint URL
                ENDPOINT_URL = 'YOUR_ENDPOINT_URL_HERE'
                try:
                    response = requests.post(ENDPOINT_URL, json=new_hackathons)
                    response.raise_for_status()  # Raise an exception if the request fails (e.g., 4xx or 5xx status codes)
                    print("Successfully sent new hackathons to the endpoint.")
                except requests.exceptions.RequestException as request_error:
                    print("Error sending hackathons to the endpoint:", request_error)

                # Insert new hackathons into MongoDB
                hackathons_collection.insert_many(new_hackathons)

            else:
                print("No new updates")

        except Exception as e:
            print("Error:", e)
            notice = {"title": "Bot Down", "link": "", "mode": "", "Date": ""}
            # Replace this placeholder with your actual endpoint URL
            ENDPOINT_URL = 'YOUR_ENDPOINT_URL_HERE'
            response = requests.post(ENDPOINT_URL, json=notice)
            print(response.text)
            break

        time.sleep(600)  # Sleep for 10 minutes (adjust as needed)

if __name__ == "__main__":
    main()