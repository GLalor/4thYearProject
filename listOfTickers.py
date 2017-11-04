from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json, urllib


def getSessionID():
	print("hello")
	urllib.request.urlcleanup()
	link = 'https://dimon.ca/snp500/' # Set destination URL here
	id = ""
	data = urllib.request.urlopen(link)
	data = json.dumps(data.read().decode())
	data = json.loads(data)
	for i in range(0,len(data)):
		if data[(23108 + i)] == '"':
			break
		id += data[(23108 + i)]
		
	return id
	
	
url = 'https://dimon.ca/api/snp500' # Set destination URL here
sessionID = getSessionID()
print(sessionID)
post_fields = {'session': sessionID}     # Set POST fields here

request = Request(url, urlencode(post_fields).encode())
data = urlopen(request).read().decode()
data = json.loads(data)
for item in data['members']:
    print(item['sym'])