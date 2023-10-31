import aiohttp
import asyncio
import logging
import os
from pymongo import MongoClient
from datetime import datetime
from lxml import html

class EventScraper:
    def __init__(self, db_uri, db_name, endpoint_url):
        # Initialize MongoDB client and database
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.hackathons_collection = self.db['prev_hackathons']
        self.endpoint_url = endpoint_url

    async def fetch_hackathons(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    content = await response.text()

            doc = html.fromstring(content)

            # Extracting hackathons data
            hackathons = []
            hackathon_elements = doc.xpath('//div[@class="sc-xyzabc"]')  # Replace with the actual XPath

            for element in hackathon_elements:
                title = element.xpath('.//h3[@class="hackathon-title"]/text()')
                link = element.xpath('.//button[@class="sc-iXxrte bRawMo"]/@href')
                mode = element.xpath('.//p[@class="hackathon-mode"]/text()')
                date = element.xpath('.//div[@class="hackathon-date"]/text()')

                if title and link and mode and date:
                    hackathon_info = {
                        "title": title[0].strip(),
                        "link": link[0].strip(),
                        "mode": mode[0].strip(),
                        "Date": date[0].strip()
                    }
                    hackathons.append(hackathon_info)

            return hackathons

        except (aiohttp.ClientError, aiohttp.ClientConnectorError) as e:
            logging.error(f"Error fetching hackathons: {e}")
            return []

    async def send_hackathons_to_endpoint(self, hackathons):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.endpoint_url, json=hackathons) as response:
                    response.raise_for_status()
                    logging.info("Successfully sent new hackathons to the endpoint.")
        except aiohttp.ClientError as e:
            logging.error(f"Error sending hackathons to the endpoint: {e}")

    def validate_hackathon_data(self, hackathon):
        # Implement data validation logic here
        # For example, you can check if certain fields are not empty or meet specific criteria
        if hackathon["title"] and hackathon["link"] and hackathon["mode"] and hackathon["Date"]:
            return True
        return False

    async def run(self):
        logging.info("Running...")

        while True:
            try:
                hackathons = await self.fetch_hackathons('https://devfolio.co/hackathons')

                # Check for new hackathons and validate them
                new_hackathons = [hackathon for hackathon in hackathons if
                                  self.validate_hackathon_data(hackathon) and
                                  not self.hackathons_collection.find_one({"title": hackathon["title"]})]

                if new_hackathons:
                    logging.info("New hackathons found:")
                    for hackathon in new_hackathons:
                        pass  # Specific actions for new hackathons can be added here
                    logging.info(new_hackathons)

                    # Send new hackathons to an endpoint asynchronously
                    await self.send_hackathons_to_endpoint(new_hackathons)

                    # Insert new hackathons into MongoDB
                    self.hackathons_collection.insert_many(new_hackathons)

                else:
                    logging.info("No new updates")

            except Exception as e:
                logging.error(f"Error: {e}")
                notice = {"title": "Bot Down", "link": "", "mode": "", "Date": datetime.now().isoformat()}
                try:
                    await self.send_hackathons_to_endpoint(notice)
                    logging.info("Successfully sent notice to the endpoint.")
                except aiohttp.ClientError as e:
                    logging.error(f"Error sending notice to the endpoint: {e}")

            await asyncio.sleep(600)  # Sleep for 10 minutes (adjust as needed)

if __name__ == "__main__":
    # Replace with your MongoDB URI, database name, and endpoint URL
    db_uri = 'mongodb://your_username:your_password@localhost:27017'
    db_name = 'hackathons_db'
    endpoint_url = 'http://localhost:8000/api/hackathons'

    event_scraper = EventScraper(db_uri, db_name, endpoint_url)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(event_scraper.run())
