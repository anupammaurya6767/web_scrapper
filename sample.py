import requests
import lxml.html
import time
import json

# Initialize an empty list to store previously seen hackathons
prev_hackathons = []

def fetch_hackathons():
    url = 'https://devfolio.co/hackathons'
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)

    div_elements = doc.xpath('//div[@class="sc-iWajrY sc-bKhNmF hackathons__StyledGrid-sc-fa04e7f9-0  bhEyGM GLpDs"]//div[@class="sc-iWajrY sc-jKDlA-D emRuhs gPHbtP"]//div[@class="sc-iWajrY deNxdR"]')
    
    hackathons = []
    
    for div_element in div_elements:
        title_element = div_element.find('.//a[@class="Link__LinkBase-sc-af40de1d-0 lkflLS"]//h3[@class="sc-tQuYZ kHbpBI"]')
        title = title_element.text_content() if title_element is not None else ""
        
        link_element = div_element.find('.//a[@class="PillButton-sc-7655a019-0 kTVrbf"]')
        link = link_element.get('href') if link_element is not None else ""
        
        mode_element = div_element.find('.//a[@class="Link__LinkBase-sc-af40de1d-0 lkflLS"]//p[@class="sc-tQuYZ iuqZMj"]')
        mode = mode_element.text_content() if mode_element is not None else ""
        
        starts = div_element.getnext().text_content()
        
        hackathon_info = {
            "title": title.strip(),
            "link": link.strip(),
            "mode": mode.strip(),
            "Date": starts.strip()
        }
        
        hackathons.append(hackathon_info)
    
    return hackathons

def main():
    global prev_hackathons  # Access the global list of previously seen hackathons
    print("Running...")
    
    while True:
        try:
            current_hackathons = fetch_hackathons()
            
            # Check for new hackathons
            new_hackathons = [hackathon for hackathon in current_hackathons if hackathon not in prev_hackathons]
            
            if new_hackathons:
                print("New hackathons found:")
                for hackathon in new_hackathons:
                    print(hackathon)
                
                # Send new hackathons to the remote endpoint here
                # url3 = 'http://localhost:8100/by'
                # response = requests.post(url3, json=new_hackathons)
                # print(response.text)
                
                # Update the list of previously seen hackathons
                prev_hackathons = current_hackathons
            
            else:
                print("No new updates")
            
        except Exception as e:
            print("Error:", e)
            notice = {"title": "Bot Down", "link": "", "mode": "", "Date": ""}
            url = 'http://20.205.15.220/last'
            response = requests.post(url, json=notice)
            print(response.text)
            break
        
        time.sleep(600)  # Sleep for 10 minutes (adjust as needed)

if __name__ == "__main__":
    main()
