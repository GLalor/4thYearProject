import json, urllib, optionChainRetrieval
from urllib.parse import urlencode
from urllib.request import Request, urlopen

def main():
	printDescription()
	url = 'https://dimon.ca/api/snp500' # Set destination URL here
	sessionID = getSessionID()
	print("SessiosessionID = ",sessionID) # Comment if on cloud
	post_fields = {'session': sessionID}     # Set POST fields here

	request = Request(url, urlencode(post_fields).encode())
	data = urlopen(request).read().decode()
	data = json.loads(data)
	for item in data['members']:
		## for testing purposes if item['sym'] == "AAPL":
			print(item['sym'])
			optionChainRetrieval.main(item['sym'])
			
			
def getSessionID():
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

def printDescription():
	print("Program to print ticker symbols of stocks in S and P 500 list")

# Stops code being run on import
if __name__ == "__main__":
    main()