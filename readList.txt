from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json, urllib
url = 'https://dimon.ca/api/snp500' # Set destination URL here
post_fields = {'session': '600-6-efbebfbcc'}     # Set POST fields here

request = Request(url, urlencode(post_fields).encode())
data = urlopen(request).read().decode()
data = json.loads(data)
for item in data['members']:
    print(item['sym'])
	