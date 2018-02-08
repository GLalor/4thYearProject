import json, datetime, random, math, time, urllib, os
from urllib.request import urlopen
#from operator import add
#import matplotlib.pyplot as plt  # mathplotlib

import findspark

findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *
sparkSession = SparkSession.builder.appName("option-pricer-write-to-hadoop").getOrCreate()
#Dictionaries for json output
option_prices = {}
results = {}
call_results = {}
put_results = {}

def main(ticker):
	option_type = "not set"
	strike_price = 0        # S(T) price at maturity
	current_value = 0		# S(0) spot price, price of stock now
	volatility = .3672 			# sigma i.e. volatility of underlying stock
	risk_free_rate = 2.1024  # mu
	expires = 55  # Number of days until maturity date

	try: # Handle page not found exceptions
		url = createYahooUrl(ticker)
		print(url)  # Prints URL to option chain
		data = urlopen(url)
		data = json.loads(data.read().decode())
		# Cutting down on loops
		for item in data['optionChain']['result']:
			if "regularMarketPrice" in item['quote']: # Test if is regularMarketPrice present will move to check if date is present in experationDates when working with dates 
				current_value = item['quote']['regularMarketPrice']
				data = item['options']
				for option in data:
					calls, puts = option['calls'], option['puts']
				# Assigning variables for calc and running sim
				for call in calls:
					option_type = "Call"
					strike_price = call['strike']	        # S(T) price at maturity
					volatility = call['impliedVolatility']
					dt = datetime.datetime.fromtimestamp(call['expiration']) - datetime.datetime.now()
					expires = dt.days
					runSimulaion(option_type, strike_price, current_value,
								volatility, risk_free_rate, expires, ticker)
					results[option_type] = call_results
				for put in puts:
					option_type = "Put"
					strike_price = put['strike']	        # S(T) price at maturity
					volatility = put['impliedVolatility']
					runSimulaion(option_type, strike_price, current_value,
									volatility, risk_free_rate, expires, ticker)
					results[option_type] = put_results
				option_prices[ticker] = results
			else:
				call_results['NA'] = "MISSING DATA"
				put_results['NA'] = "MISSING DATA"
				results[option_type] = call_results
				results[option_type] = put_results
				option_prices[ticker] = results
		with open('optionPrices.json', 'w') as outfile:
			json.dump(option_prices,outfile)
		
		writeResultHive()

	except urllib.error.HTTPError as err:
		if err.code == 404:
			print("Page not found for ticker "+ ticker +"!")
		elif err.code == 403:
			print("Access denied!")
		else:
			print("Something happened! Error code", err.code)
	except urllib.error.URLError as err:
		print("Some other error happened:", err.reason)
		

def runSimulaion(option_type, strike_price, current_value, volatility, risk_free_rate, expires, ticker):
	start_date = datetime.date.today()
	num_simulations = 10000
	option_prices = []
	for x in range(0, 5):
		# W(T) Wiener process/Brownian motion  = math.sqrt(T) * random.gauss(0, 1.0)
		# sequential approach, calculate option price every day until expiry
		
		times = []
		# 1 .. expires inclusive
		for i in range(1, expires + 1):
			# results from each simulation step
			sim_results = []
			T = i / 365               # days in the future
			times.append(i)
			for j in range(num_simulations):
				sim_results.append(sim_option_price(time.time() + j, current_value,
										risk_free_rate, volatility, T, strike_price, option_type))

			# e to the power of ()
			discount_factor = math.exp(-risk_free_rate * T)
			option_prices.append(
			discount_factor * (sum(sim_results) / float(num_simulations)))
			if option_type == "Call":
				call_results[(str(start_date + datetime.timedelta(days=i)))] = option_prices
				#print(ticker, " ", option_type, " ", "Option Price ",
				#option_prices[i - 1], " at ", start_date + datetime.timedelta(days=i))
			else:
				put_results[(str(start_date + datetime.timedelta(days=i)))] = option_prices
				#print(ticker, " ", option_type, " ", "Option Price ",
				#option_prices[i - 1], " at ", start_date + datetime.timedelta(days=i))

	# Code to plot results to a graph
	# plt.plot(times, option_prices)
	# plt.xlabel('T')
	# plt.ylabel('Option Prices')
	# plt.show()

# european or asian call price
def call_payoff(asset_price, strike_price):
	return max(0.0, asset_price - strike_price)


def put_payoff(asset_price, strike_price):
	return max(0.0, strike_price - asset_price)

# simulate the option price
def sim_option_price(seed, current_value, risk_free_rate, volatility, T, strike_price, option_type):
	random.seed(seed)
	asset_price = current_value * \
	math.exp((risk_free_rate - .5 * volatility**2) * T +
	volatility * math.sqrt(T) * random.gauss(0, 1.0))
	if option_type == "Call":
		return call_payoff(asset_price, strike_price)
	else:
		return put_payoff(asset_price, strike_price)

def createYahooUrl(optionTicker):
	try:
		if "." in optionTicker:  # some tickers in list have "." when not needed
			optionTicker = optionTicker.replace(".", "")  # Removing "."

		url = "https://query2.finance.yahoo.com/v7/finance/options/"+ optionTicker
		data = urlopen(url)
		data = json.loads(data.read().decode())
		expirationDates = data['optionChain']['result'][0]['expirationDates']
		for item in expirationDates:
			dt = datetime.datetime.fromtimestamp(item) - datetime.datetime.now()
			if dt.days > 0: # should run he day before bu is seen as 0 days and number of hours
				expDate = item
				break
		return url + "?date=" + str(expDate)
	except urllib.error.HTTPError as err:
		if err.code == 404:
			print("Page not found!")
		elif err.code == 403:
			print("Access denied!")
		else:
			print("Something happened! Error code", err.code)
	except urllib.error.URLError as err:
		print("Some other error happened:", err.reason)
	

def writeResultHive():
    option_prices_data = sparkSession.read.json('optionPrices.json')
    option_prices_data.write.save('E:\ProjectDB', format='json', mode='append')

    # sparkSession.sql("DROP TABLE IF EXISTS option_prices_data_table")
    # sparkSession.table("option_prices_data").write.saveAsTable("option_prices_data_table")
    #  USE TO TEST DB
    resultsHiveDF = sparkSession.read.format('json').load('E:\ProjectDB') 
    resultsHiveDF.show(1)

# Stops code being run on import
if __name__ == "__main__":
	main()