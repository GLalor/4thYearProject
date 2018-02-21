import findspark

findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *
sparkSession = SparkSession.builder.appName(
    "option-pricer-write-to-hadoop").getOrCreate()


def writeResultHive():
    option_prices_data = sparkSession.read.json('optionPrices.json')
    option_prices_data.write.save('E:\ProjectDB', format='json', mode='append')

    # sparkSession.sql("DROP TABLE IF EXISTS option_prices_data_table")
    # sparkSession.table("option_prices_data").write.saveAsTable("option_prices_data_table")
    #  USE TO TEST DB
    resultsHiveDF = sparkSession.read.format('json').load('E:\ProjectDB')
    resultsHiveDF.show(1)