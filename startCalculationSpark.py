import json, urllib, optionCalculationSpark, time, findspark
import getSNPList
import riskRateRetrieval
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
	data = getSNPList.main()
	rates = riskRateRetrieval.main()
	for item in data['members']:
		symbols.append(item['sym'])

	with open('SnPList.json', 'w') as outfile:
			json.dump(data,outfile)

	symbols = sc.parallelize(symbols)
	#print(symbols.collect())
	result = symbols.map(lambda sym: optionCalculationSpark.main(sym,rates))
	print(result.collect())
	print("******** finsihed in %s seconds ********" % (time.time() -start_time))



def printDescription():
	print("Program to retrive and print the ticker symbols of stocks in S and P 500 list")

# Stops code being run on import
if __name__ == "__main__":
	main()