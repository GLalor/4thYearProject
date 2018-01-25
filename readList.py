import json, urllib, optionChainRetrieval, time, findspark
from bs4 import BeautifulSoup 
from urllib.parse import urlencode
from urllib.request import Request, urlopen

findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
# Starting and configuring spark session
conf = SparkConf().setAppName('OptionPricer')
spark = SparkSession \
    .builder \
    .appName("Spark opion pricer") \
    .config(conf=conf) \
    .getOrCreate()

#sc = SparkContext(conf=conf)

#sc.addPyFile("/Users/graha/Documents/4th%20year/Project/Vanilla-Option-Pricer/optionChainRetrieval.py")
def main():
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

	sparkData = spark.read.json("./SnPList.json")
	#for item in data['members']:
	# 	## for testing purposes if item['sym'] == "AAPL":
	# 		print(item['sym'])
	sparkData.createOrReplaceTempView("Members")
	snpMembers = spark.sql("SELECT members.sym FROM Members")
	snpMembers.show()
	#parallelData = spark.parallelize(sparkData).filter(lambda item: item['members'])
	#result = parallelData.map(main())
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