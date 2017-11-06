import json
import datetime
import random 
import math 
import time
import datetime
from operator import add
import matplotlib.pyplot as plt                         #mathplotlib
import sys
from urllib.request import urlopen

def main(ticker):
	STRIKE_PRICE = 0        # S(T) price at maturity
	CURRENT_VALUE =0		# S(0) spot price, price of stock now
	VOLATILITY = .3672 			# sigma i.e. volatility of underlying stock
	RISK_FREE_RATE = 2.1024 # mu
	NO_SIMULATIONS = 10000
	START_DATE = datetime.date.today()
	EXPIRES = 55	# Number of days until maturity date
	if "." in ticker: # some tickers in list have "." when not needed
		ticker = ticker.replace(".", "") # Removing "."
	url = "https://query2.finance.yahoo.com/v7/finance/options/"
	url += ticker

	print(url)	# Prints URL to option chain

	data = urlopen(url)
	data = json.loads(data.read().decode())
	for x in data['optionChain']['result']:
		CURRENT_VALUE = x['quote']['regularMarketPrice']
		for y in x['options']:
			if not y['calls']:
				for option in y['calls']:
					STRIKE_PRICE = option['strike']	        # S(T) price at maturity
					#VOLATILITY = option['impliedVolatility']	
				
	for x in range(0,5):
		# W(T) Wiener process/Brownian motion  = math.sqrt(T) * random.gauss(0, 1.0)
		# sequential approach, calculate option price every day until expiry
		option_prices = []
		times = []
		for i in range(1, EXPIRES + 1):                                                 # 1 .. EXPIRES inclusive
				sim_results = []                                                        # results from each simulation step
				T = i/365               # days in the future
				times.append(i)
				for j in range(NO_SIMULATIONS):
					sim_results.append(sim_option_price(time.time() + j,CURRENT_VALUE,
														RISK_FREE_RATE, VOLATILITY,T,STRIKE_PRICE))

				discount_factor = math.exp(-RISK_FREE_RATE * T)                         # e to the power of ()
				option_prices.append(discount_factor * (sum(sim_results) / float(NO_SIMULATIONS)))
				print (ticker," ","Option Price ", option_prices[i-1], " at ", START_DATE + datetime.timedelta(days=i))
		# Code to plot results to a graph
		# plt.plot(times, option_prices)
		# plt.xlabel('T')
		# plt.ylabel('Option Prices')
		# plt.show()	

# european or asian call price
def call_payoff(asset_price, STRIKE_PRICE): 
	return max(0.0, asset_price - STRIKE_PRICE)

# simulate the option price
def sim_option_price(seed,CURRENT_VALUE,RISK_FREE_RATE,VOLATILITY,T,STRIKE_PRICE): 
	random.seed(seed) 
	asset_price = CURRENT_VALUE * math.exp((RISK_FREE_RATE - .5 * VOLATILITY**2) * T + VOLATILITY * math.sqrt(T) * random.gauss(0,1.0)) 
	return call_payoff(asset_price, STRIKE_PRICE)

# Stops code being run on import	
if __name__ == "__main__":
	main()
			
			