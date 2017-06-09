from bs4 import BeautifulSoup
import requests
import requests.exceptions
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def ping(u):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    page = requests.get(u)
    return page

def scrape(u):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    page = requests.get(u)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')
    paragraphs = soup.find_all("p")

    bigList = []

    for para in paragraphs:
        para = para.getText()
        para = para.encode('ascii', 'ignore')
        para = para.decode('ascii', 'ignore')
        bigList.append(para)

    culledList = []

    cnt = 0

    week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    while(True):
        cnt += 1
        if cnt < 4:
            continue

        mtg = {}

        if cnt+6 > len(bigList):
            break

        for day in week:
            if day in bigList[cnt]:
                mtg['date'] = bigList[cnt]
                mtg['time'] = bigList[cnt+1]
                mtg['agenda'] = bigList[cnt+2]
                mtg['location'] = bigList[cnt+5].replace('(',"").replace(')',"")
                culledList.append(mtg)
                cnt += 5

    return culledList

test = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
randy = test[random.randint(0,len(test)-10)]
preface = "Hi test monkey, here's a random meeting: "
mess = preface+randy['date']+" "+randy['time']+" "+randy['agenda']
print(mess)



