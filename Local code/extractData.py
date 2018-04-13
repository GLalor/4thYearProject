import findspark
findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *
sparkSession = SparkSession.builder.appName(
    "option-pricer-write-to-hadoop").getOrCreate()

# change 'E:\ProjectDB' depending on location written to in writeToHDFS.py
resultsHiveDF = sparkSession.read.format('json').load('E:\ProjectDB')
resultsHiveDF.createOrReplaceTempView("optionData")


def getTickerSymbols():
    """ Function to turn a sored list of Ticker sysmbols """
    tickers = sparkSession.sql("SELECT Ticker FROM optionData").collect()
    tickerSymbols = []
    for i in tickers:  # remove Row(Ticker=) from ticker
        tickerSymbols.append(i['Ticker'])
    tickerSymbols.sort()
    return tickerSymbols


def getNumberOfDays(ticker):
    """ Function to turn an array of ints for number of days before expDate
        eg. number of says is 5 returns [1,2,3,4,5] """
    numOfDays = sparkSession.sql(
        "SELECT NumberOfDays FROM optionData WHERE Ticker Like '" +
        ticker +
        "'").collect()
    numDaysArr = []
    for i in range(1, numOfDays[0]['NumberOfDays'] + 2):
        numDaysArr.append(i)
    return numDaysArr


def getOptionPricesByTicker(ticker):
    """ Function to get prices based on a specific ticker symbol """
    return sparkSession.sql(
        "SELECT Prices FROM optionData WHERE Ticker Like '" +
        ticker +
        "'").collect()


# Probably have to change if more than 2 lines as graph code might crash
# TEST THIS
def getRiskRateForGraph(ticker):
    ratesArr = []
    count = 1
    riskFreeRates = sparkSession.sql(
        "SELECT riskFreeRates FROM optionData WHERE Ticker Like '" +
        ticker +
        "'").collect()
    for rate in riskFreeRates[0]['riskFreeRates']:
        ratesArr.append(rate)
    return ratesArr


def getCallStrikePricesByTicker(ticker):
    """ Function to return a sorted list of strike prices for a particual ticker passes as a parameter """
    prices = sparkSession.sql(
        "SELECT Prices FROM optionData WHERE Ticker Like '" +
        ticker +
        "'").collect()
    strikePricesArray = []
    for i in prices[0]['Prices']:
        if i['Call'] is not None and i['StrikePrice'] not in strikePricesArray:
            strikePricesArray.append(i['StrikePrice'])
    strikePricesArray.sort()
    return strikePricesArray


def getPutStrikePricesByTicker(ticker):
    """ Function to return a sorted list of strike prices for a particual ticker passes as a parameter """
    prices = sparkSession.sql(
        "SELECT Prices FROM optionData WHERE Ticker Like '" +
        ticker +
        "'").collect()
    strikePricesArray = []
    for i in prices[0]['Prices']:
        if i['Put'] is not None and i['StrikePrice'] not in strikePricesArray:
            strikePricesArray.append(i['StrikePrice'])
    strikePricesArray.sort()
    return strikePricesArray


def getPricesByOptionType(optionPrices, optionType):
    """ Function to return a list of calls or puts for a set of options passed as a parameter in row format """
    callPrices = []
    for i in optionPrices[0][0]:
        if i[optionType] is not None:
            callPrices.append(i)
    return callPrices


def getCallPrices(optionPrices):
    """ Function to return a list of call prices for a set of options passed as a parameter"""
    callPrices = []
    for i in optionPrices[0][0]:
        if i['Call'] is not None:
            callPrices.append(i['Call'])
    return callPrices


def getPutPrices(optionPrices):
    """ Function to return a list of put prices for a set of options passed as a parameter"""
    putPrices = []
    for i in optionPrices[0][0]:
        if i['Put'] is not None:
            putPrices.append(i['Put'])
    return putPrices


def convertPricesToDic(opPrices):
    """ Funtion to convert list of all prices to a dictionary for graphing """
    prices = {}
    count = 1
    for i in opPrices:
        priceArr = []
        for x in i:
            if x is not None:
                priceArr.append(x)
        prices['opt' + str(count)] = (priceArr.copy())
        count = count + 1
    return prices


def getCallsPricesFromFullRow(optionPrices):
    callPrices = []
    for i in optionPrices:
        if i['Call'] is not None:
            callPrices.append(i[0])
    return callPrices


def getPutsPricesFromFullRow(optionPrices):
    putPrices = []
    for i in optionPrices:
        if i['Put'] is not None:
            putPrices.append(i[1])
    return putPrices


def getPricesByStrike(optionPrices, strike, optionType):
    allPrices = []
    for i in optionPrices:
        if i is not None and i['StrikePrice'] == strike:
            allPrices.append(i[optionType])
    return allPrices


def getPricesByStrikeAndRate(optionPrices, strike, RiskFreeRate):
    allPrices = []
    for i in optionPrices[0][0]:
        if i is not None and i['StrikePrice'] == strike and i['RiskFreeRate'] == RiskFreeRate:
            allPrices.append(i[0])
    return allPrices


def getPricesByRiskFreeRateAndStrike(optionPrices, RiskFreeRate, strikePrice):
    allPrices = []
    for i in optionPrices[0][0]:
        if i['RiskFreeRate'] == RiskFreeRate and i['StrikePrice'] == strikePrice:
            allPrices.append(i)
    return allPrices
