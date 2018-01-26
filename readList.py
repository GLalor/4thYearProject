import json, urllib, optionChainRetrieval, time, findspark
from bs4 import BeautifulSoup 
from urllib.parse import urlencode
from urllib.request import Request, urlopen

findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
# Starting and configuring spark session
conf = SparkConf().setMaster("local[4]").setAppName('OptionPricer')
# spark = SparkSession \
#     .builder \
#     .appName("Spark opion pricer") \
#     .config(conf=conf) \
#     .getOrCreate()

sc = SparkContext(conf=conf)

#sc.addPyFile("/Users/graha/Documents/4th%20year/Project/Vanilla-Option-Pricer/optionChainRetrieval.py")
def main():
	symbols = []
	start_time = time.time()
	printDescription()
	url = 'https://dimon.ca/api/snp500' # Set destination URL here
	sessionID = getSessionID()
	print("SessiosessionID = ",sessionID) # Comment if on cloud
	post_fields = {'session': sessionID}     # Set POST fields here

	request = Request(url, urlencode(post_fields).encode())
	data = urlopen(request).read().decode()
	data = json.loads(data)
	with open('SnPList.json', 'w') as outfile:
			json.dump(data,outfile)
	for item in data['members']:
		symbols.append(item['sym'])
		# Use line below to test option errors
		#optionChainRetrieval.main(item['sym'])
	
	symbols = sc.parallelize(symbols)
	#print(symbols.collect())
	result = symbols.map(lambda sym: optionChainRetrieval.main(sym))
	print(result.collect())
	print("******** finsihed in %s seconds ********" % (time.time() -start_time))

def getSessionID():
	urllib.request.urlcleanup()
	link = 'https://dimon.ca/snp500/' # Set destination URL here
	id = ""
	data = urllib.request.urlopen(link)
	data = BeautifulSoup(data, "html.parser")
	id = data.find('input', attrs={'name':'session'}).get('value')
		
	return id

def printDescription():
	print("Program to retrive and print the ticker symbols of stocks in S and P 500 list")

# Stops code being run on import
if __name__ == "__main__":
    main()