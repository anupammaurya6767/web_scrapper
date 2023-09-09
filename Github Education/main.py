import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

class Events:
 

    def __init__(self):
        # Initialize MongoDB connection
        self.client = MongoClient('mongodb://your_username:your_password@localhost:27017')
        self.db = self.client['your_database_name']
        self.events_collection = self.db['events']

    def get_events(self):
        url = "https://education.github.com/events"
        events_data = {"events": []}
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            events = soup.find_all("a", class_="d-flex js-landing-page-link event-card")

            for e in events:
                tags_list = []
                title = e.find("h3", class_="h5").getText().strip()
                img = e.find("img")["src"]
                try:
                    desc = (
                        e.find("p", class_="my-3 short-event color-fg-muted")
                        .getText()
                        .strip()
                    )
                except:
                    desc = ""
                base = e.find_all("p", class_="color-fg-muted text-small")
                date = base[0].getText().strip()
                loc = base[1].getText().strip()
                lang = (
                    e.find("p", class_="color-fg-muted text-small mb-3")
                    .getText()
                    .strip()
                )
                labels = e.find_all(
                    "span", class_="Label--small Label--blue-standard mr-2"
                )
                for l in labels:
                    tags_list.append(l.getText().strip())
                link = e["href"]

                events_data["events"].append(
                    {
                        "title": title,
                        "image_url": img,
                        "description": desc,
                        "date": date,
                        "location": loc,
                        "language": lang,
                        "tags": tags_list,
                        "link": link,
                    }
                )
            return events_data["events"]
        except:
            return None

    def check_and_send_events(self):
        """
        Periodically check for new events and send them to an endpoint.
        """
        while True:
            try:
                current_events = self.get_events()

                # Check for new events
                new_events = [event for event in current_events if not self.events_collection.find_one(event)]

                if new_events:
                    print("New events found:")
                    for event in new_events:
                        pass  # You can perform any specific actions here for new events
                    print(new_events)

                    # Replace this placeholder with your actual endpoint URL
                    ENDPOINT_URL = 'YOUR_ENDPOINT_URL_HERE'
                    try:
                        response = requests.post(ENDPOINT_URL, json=new_events)
                        response.raise_for_status()  # Raise an exception if the request fails (e.g., 4xx or 5xx status codes)
                        print("Successfully sent new events to the endpoint.")
                    except requests.exceptions.RequestException as request_error:
                        print("Error sending events to the endpoint:", request_error)

                    # Insert new events into MongoDB
                    self.events_collection.insert_many(new_events)

                else:
                    print("No new events")

            except Exception as e:
                print("Error:", e)
                notice = {"title": "Bot Down", "link": "", "mode": "", "Date": ""}
                # Replace this placeholder with your actual endpoint URL
                ENDPOINT_URL = 'YOUR_ENDPOINT_URL_HERE'
                response = requests.post(ENDPOINT_URL, json=notice)
                print(response.text)
                break

            time.sleep(600)  # Sleep for 10 minutes (adjust as needed)

# Create an instance of the Events class and start checking for new events
events_instance = Events()
events_instance.check_and_send_events()
