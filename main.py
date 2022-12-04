import requests
import lxml.html
import time
import json

html = requests.get('https://www.igdtuw.ac.in/')
doc = lxml.html.fromstring(html.content)

prev = doc.xpath(
    '//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@class="ENABox Events"]/li/a'
)[1]

print("running")
while True:
    time.sleep(30)
    prev_title =  doc.xpath(
                '//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@class="ENABox Events"]/li/a/text()'
            )[0]
    
    prev_link = doc.xpath(
                '//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@class="ENABox Events"]/li/a/@href'
            )[0]
    html3 = requests.get("https://www.igdtuw.ac.in/"+prev_link)                                                             
    doc3 = lxml.html.fromstring(html3.content)                                                                         
    prev_release_data_link = doc3.xpath('//div[@class="headingPara"]//table[@class="facultyTable"]//a/@href')[0]
    prev_notice = {                                                                                                         
                 "title": prev_title,                                                                                                
                 "link": "https://www.igdtuw.ac.in/" + prev_release_data_link,                                                   
                 "tab": "Notices/Circulars"                                                                                     
             } 
    
    url3 = 'http://20.205.15.220/last'
    data3 = json.dumps(prev_notice)
    x3 = requests.post(url3, json=prev_notice)
    print(x3.text)
    try:
        prev_hash = hash(prev)
        new_release = doc.xpath(
            '//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@class="ENABox Events"]/li/a'
        )[0]
        new_hash = hash(new_release)

        if (new_hash != prev_hash):
            title = doc.xpath(
                '//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@class="ENABox Events"]/li/a/text()'
            )[0]
            link = doc.xpath(
                '//div[@class="container"]/div[@class="row"]//div[@class="col-sm-7"]/div[@class="bigBox"]/div[@class="bigBoxDiv"]/ul[@class="ENABox Events"]/li/a/@href'
            )[0]


             html2 = requests.get("https://www.igdtuw.ac.in/"+link)                                                             
             doc2 = lxml.html.fromstring(html2.content)                                                                         
             new_release_data_link = doc2.xpath('//div[@class="headingPara"]//table[@class="facultyTable"]//a/@href')[0]                                                                                              
             notice = {                                                                                                         
                 "title": title,                                                                                                
                 "link": "https://www.igdtuw.ac.in/" + new_release_data_link,                                                   
                 "tab": "Notices/Circulars"                                                                                     
             }                                                                                                                  
            url = 'http://20.205.15.220/by'
            data = json.dumps(notice)
            x = requests.post(url, json=notice)
            print(x.text)
            print(notice)
            prev = new_release

        else:
            print("no update")

        time.sleep(10)
        continue

    except Exception as e:
        print(e)
        notice = {"title": "Bot Down", "link": "", "tab": ""}
        url = 'http://20.205.15.220/by
        x = requests.post(url, json=notice)
        break
