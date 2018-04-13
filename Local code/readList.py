import json
import urllib
import optionPriceCuda
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def getSessionID():
    urllib.request.urlcleanup()
    link = 'https://dimon.ca/snp500/'  # Set destination URL here
    id = ""
    data = urllib.request.urlopen(link)
    data = BeautifulSoup(data, "html.parser")
    id = data.find('input', attrs={'name': 'session'}).get('value')
    return id


def printDescription():
    print("Program to print ticker symbols of stocks in S and P 500 list")


# Stops code being run on import
if __name__ == "__main__":
    start_time = time.time()
    printDescription()
    url = 'https://dimon.ca/api/snp500'  # Set destination URL here
    sessionID = getSessionID()
    print("SessiosessionID = ", sessionID)  # Comment if on cloud
    post_fields = {'session': sessionID}     # Set POST fields here

    request = Request(url, urlencode(post_fields).encode())
    data = urlopen(request).read().decode()
    data = json.loads(data)
    for item in data['members']:
            # if item['sym'] == "AAPL":
        print(item['sym'])
        optionPriceCuda.main(item['sym'])
    print(
        "******** finsihed in %s seconds ********" %
        (time.time() - start_time))
