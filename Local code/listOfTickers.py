import json
import urllib
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def main():
    printDescription()  # Only if running on home device! Comment if on cloud
    url = 'https://dimon.ca/api/snp500'  # Set destination URL here
    sessionID = getSessionID()
    print("SessiosessionID = ", sessionID)  # Comment if on cloud
    post_fields = {'session': sessionID}     # Set POST fields here

    request = Request(url, urlencode(post_fields).encode())
    data = urlopen(request).read().decode()
    data = json.loads(data)
    i = 0
    for item in data['members']:
        i = i + 1
        print(item['sym'], " ", i)


def printDescription():
    print("Program to print ticker symbols of stocks in S and P 500 list")


def getSessionID():             # Scrapping page for sessionID to access api/snp500
    id = ""
    urllib.request.urlcleanup()  # clean cache from page
    link = 'https://dimon.ca/snp500/'  # Set destination URL here
    data = urllib.request.urlopen(link)
    data = json.dumps(data.read().decode())
    data = json.loads(data)
    for i in range(0, len(data)):
        if data[(23108 + i)] == '"':
            break
        id += data[(23108 + i)]

    return id


# Stops code being run on import
if __name__ == "__main__":
    main()