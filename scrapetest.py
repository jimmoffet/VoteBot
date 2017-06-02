from bs4 import BeautifulSoup
import requests
import requests.exceptions
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def scrape(u):

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    page = requests.get(u)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')
    paragraphs = soup.find_all("p")

    bigList = []

    for para in paragraphs:
        para = para.getText()
        para = para.encode('ascii', 'ignore')
        bigList.append(para)

    culledList = []

    cnt = 0
    
    for para in bigList:
        stop = False
        cnt += 1
        if cnt < 4:
            continue

        culledDict = {}

        culledDict['date'] = bigList[cnt].decode('ascii', 'ignore')
        culledDict['time'] = bigList[cnt+1].decode('ascii', 'ignore')
        culledDict['agenda'] = bigList[cnt+2].decode('ascii', 'ignore')
        culledDict['location'] = bigList[cnt+5].decode('ascii', 'ignore').replace('(',"").replace(')',"")

        culledList.append(culledDict)
   
        stopstr = 'and reasonable modifications in policies and procedures to persons with disabilities upon request. Contact the Office of the City Clerk'
        
        for i in range(5,10):
            if stopstr in str(bigList[cnt+i]):
                stop = True
        if stop:
            break
        if cnt+9 > len(bigList):
            break
        cnt += 8

    return culledList

test = scrape('http://cambridgema.iqm2.com/Citizens/Detail_LegalNotice.aspx?ID=1008')
print(test)
