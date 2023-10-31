import requests
import lxml.html
import time
import json

# Function to extract the latest notice information
def get_latest_notice(doc):
    title = doc.xpath('//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@class="ENABox Events"]/li/a/text()')[0]
    link = doc.xpath('//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@="ENABox Events"]/li/a/@href')[0]
    return {
        "title": title,
        "link": "https://www.igdtuw.ac.in/" + link,
        "tab": "Notices/Circulars"
    }

# Your endpoint URL
endpoint_url = 'http://your_endpoint'

# Initialize previous notice
prev_notice = get_latest_notice(lxml.html.fromstring(requests.get('https://www.igdtuw.ac.in/').content))

print("Running")
while True:
    try:
        new_notice = get_latest_notice(lxml.html.fromstring(requests.get('https://www.igdtuw.ac.in/').content))

        if new_notice != prev_notice:
            # Send the new notice to your endpoint
            response = requests.post(endpoint_url, json=new_notice)
            print(new_notice)

            if response.status_code == 200:
                prev_notice = new_notice
            else:
                print("Failed to send notice to the endpoint")

        else:
            print("No update")

        time.sleep(10)  # The program will run every 10 seconds.

    except Exception as e:
        print(e)
        notice = {"title": "Bot Down", "link": "", "tab": ""}
        response = requests.post(endpoint_url, json=notice)
        break
