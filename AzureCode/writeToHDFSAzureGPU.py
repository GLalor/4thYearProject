import findspark

findspark.init("/home/gpucalc/spark-2.2.1-bin-hadoop2.7")
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *
sparkSession = SparkSession.builder.appName(
    "option-pricer-write-to-hadoop").getOrCreate()

# Set azure blob config to write to
sparkSession._jsc.hadoopConfiguration().set("fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem")
sparkSession._jsc.hadoopConfiguration().set("fs.azure.account.key.optiondatastorage.blob.core.windows.net", "X6s7Fmxhb6TM/+OhvIl0rNHhOQebO701I1dVdzaW6pKvdi9uVKFgRyW771hrvfCf1TgRA9v+5D7p76pw9ROR6g==")
baseDir = "wasb://optiondata-2018-04-10t08-21-24-836z@optiondatastorage.blob.core.windows.net/GPUData/"

def writeResultHive(): # Write results as blobs in azure 
    option_prices_data = sparkSession.read.json('optionPrices.json')
    option_prices_data.write.save(baseDir, format='json', mode='append')
