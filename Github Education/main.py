import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

class EventScraper:
    def __init__(self, db_uri, db_name, endpoint_url):
        # Initialize MongoDB connection
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.events_collection = self.db['events']
        self.endpoint_url = endpoint_url

    def get_events(self):
        try:
            url = "https://education.github.com/events"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            events_data = []

            for e in soup.find_all("a", class_="d-flex js-landing-page-link event-card"):
                title = e.find("h3", class_="h5").get_text(strip=True)
                img = e.find("img")["src"]
                desc = e.find("p", class_="my-3 short-event color-fg-muted").get_text(strip=True, default="")
                base = e.find_all("p", class_="color-fg-muted text-small")
                date, loc = [item.get_text(strip=True) for item in base[:2]]
                lang = e.find("p", class_="color-fg-muted text-small mb-3").get_text(strip=True)
                tags_list = [l.get_text(strip=True) for l in e.find_all("span", class_="Label--small Label--blue-standard mr-2")]
                link = e["href"]

                events_data.append({
                    "title": title,
                    "image_url": img,
                    "description": desc,
                    "date": date,
                    "location": loc,
                    "language": lang,
                    "tags": tags_list,
                    "link": link,
                })

            return events_data

        except requests.exceptions.RequestException as request_error:
            print("Error fetching events:", request_error)
            return []

    def check_and_send_events(self):
        while True:
            try:
                current_events = self.get_events()
                new_events = [event for event in current_events if not self.events_collection.find_one(event)]

                if new_events:
                    print("New events found:")
                    for event in new_events:
                        pass  # Specific actions for new events can be added here
                    print(new_events)

                    try:
                        response = requests.post(self.endpoint_url, json=new_events)
                        response.raise_for_status()
                        print("Successfully sent new events to the endpoint.")
                    except requests.exceptions.RequestException as request_error:
                        print("Error sending events to the endpoint:", request_error)

                    self.events_collection.insert_many(new_events)

                else:
                    print("No new events")

            except Exception as e:
                print("Error:", e)
                notice = {"title": "Bot Down", "link": "", "mode": "", "Date": ""}
                response = requests.post(self.endpoint_url, json=notice)
                print(response.text)
                break

            time.sleep(600)  # Sleep for 10 minutes (adjust as needed)

if __name__ == "__main__":
    # Replace with your MongoDB URI, database name, and endpoint URL
    db_uri = 'mongodb://your_username:your_password@localhost:27017'
    db_name = 'your_database_name'
    endpoint_url = 'YOUR_ENDPOINT_URL_HERE'
    
    event_scraper = EventScraper(db_uri, db_name, endpoint_url)
    event_scraper.check_and_send_events()
