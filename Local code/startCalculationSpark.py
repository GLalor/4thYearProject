import json
import urllib
import optionCalculationSpark
import time
import findspark
import getSNPList
import riskRateRetrieval
import pandas
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# set to install location of spark and hadoop as prebuilt
findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
# Starting and configuring spark session
conf = SparkConf().setMaster("local[4]").setAppName('OptionPricer')
sc = SparkContext(conf=conf)


def main():
    symbols = []
    start_time = time.time()
    printDescription()
    data = getSNPList.main()
    rates = riskRateRetrieval.main()
    for item in data['members']:
        symbols.append(item['sym'])

    symbols = sc.parallelize(symbols)
    result = symbols.map(lambda sym: optionCalculationSpark.main(sym, rates))
    result.collect()

    spark = SparkSession(sc)
    option_prices_data = spark.read.json('optionPrices.json')
    option_prices_data.write.save(
        'E:\ProjectDB6',
        format='json',
        mode='append')  # set DB location
    print(
        "******** finsihed in %s seconds ********" %
        (time.time() - start_time))


def printDescription():
    print("Program to retrive and print the ticker symbols of stocks in S and P 500 list")


# Stops code being run on import
if __name__ == "__main__":
    main()
