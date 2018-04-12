import json
import urllib
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def main():
    url = 'https://dimon.ca/api/snp500'  # Set destination URL here
    sessionID = getSessionID()
    print("SessiosessionID = ", sessionID)  # Comment if on cloud
    post_fields = {'session': sessionID}     # Set POST fields here

    request = Request(url, urlencode(post_fields).encode())
    data = urlopen(request).read().decode()
    data = json.loads(data)
    return data

# gets required session ID from base html file (its hardcoded in html file)
def getSessionID():
    urllib.request.urlcleanup()  # removes any cache, cookies etc
    link = 'https://dimon.ca/snp500/'  # Set destination URL here
    id = ""
    data = urllib.request.urlopen(link)
    data = BeautifulSoup(data, "html.parser")
    id = data.find('input', attrs={'name': 'session'}).get('value')
    return id


# Stops code being run on import
if __name__ == "__main__":
    main()