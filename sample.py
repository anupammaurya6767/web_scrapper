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

    div_elements = doc.xpath(
        '//div[@class="sc-iWajrY sc-bKhNmF hackathons__StyledGrid-sc-fa04e7f9-0  bhEyGM GLpDs"]//div[@class="sc-egNfGp yTbeG CompactHackathonCard__StyledCard-sc-4a10fa2a-0 ihpCnk"]')

    hackathons = []
    #div_element_str = lxml.html.tostring(div_elements, encoding='utf-8', pretty_print=True).decode('utf-8')
    # print(div_elements)
    for div_element in div_elements:
        title_element = div_element.find(
            './/a[@class="Link__LinkBase-sc-af40de1d-0 lkflLS"]//h3[@class="sc-tQuYZ kHbpBI"]')
        title = title_element.text_content() if title_element is not None else ""


        #
        link_element = div_element.find('.//a[@class="PillButton-sc-7655a019-0 kTVrbf"]')
        link = link_element.get('href') if link_element is not None else ""


        #
        mode_element = div_element.find(
             './/div[@class="sc-iWajrY deNxdR"]//p[@class="sc-tQuYZ EdbiX"]')
        mode = mode_element.text_content() if mode_element is not None else ""


        #
        starts_element = div_element.find(
             './/div[@class="sc-iWajrY sc-jKDlA-D  fIIKMx"]')
        starts_fill = starts_element.text_content() if mode_element is not None else ""
        starts = starts_fill[-8:]
        if(starts[-5:] != "Ended"):
            hackathon_info = {
                "title": title.strip(),
                "link": link.strip(),
                "mode": mode.strip(),
                "Date": starts.strip()
            }

            hackathons.append(hackathon_info)
        #
        #


    return hackathons


def main():
    global prev_hackathons  # Access the global list of previously seen hackathons
    print("Running...")

    while True:
        try:
            fetch_hackathons()
            current_hackathons = fetch_hackathons()

            # Check for new hackathons
            new_hackathons = [hackathon for hackathon in current_hackathons if hackathon not in prev_hackathons]

            if new_hackathons:
                print("New hackathons found:")
                for hackathon in new_hackathons:
                    pass
                print(new_hackathons)
                # Send new hackathons to the remote endpoint here
                url3 = 'http://165.22.119.151:8100/by'
                response = requests.post(url3, json=new_hackathons)
                print(response.text)

                # Update the list of previously seen hackathons
                prev_hackathons = current_hackathons

            else:
                print("No new updates")

        except Exception as e:
            print("Error:", e)
            notice = {"title": "Bot Down", "link": "", "mode": "", "Date": ""}
            url = 'http://165.22.119.151:8100/by'
            response = requests.post(url, json=notice)
            print(response.text)
            break

        time.sleep(6)  # Sleep for 10 minutes (adjust as needed)


if __name__ == "__main__":
    main()
