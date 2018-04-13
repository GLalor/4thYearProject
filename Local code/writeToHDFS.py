import findspark

findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *
sparkSession = SparkSession.builder.appName(
    "option-pricer-write-to-hadoop").getOrCreate()

# change 'E:\ProjectDB' to a suitable drive on computer


def writeResultHive():
    option_prices_data = sparkSession.read.json('optionPrices.json')
    option_prices_data.write.save('E:\ProjectDB', format='json', mode='append')
    #  USE TO TEST DB
    resultsHiveDF = sparkSession.read.format('json').load('E:\ProjectDB')
    resultsHiveDF.show(1)
