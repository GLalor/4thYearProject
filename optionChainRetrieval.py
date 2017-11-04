
from urllib.request import urlopen
import json

import datetime
import random 
import math 
import time
import datetime
from operator import add
import matplotlib.pyplot as plt                         #mathplotlib
import sys

def run(ticker):
	if "." in ticker:
		ticker = ticker.replace(".", "")
	url = "https://query2.finance.yahoo.com/v7/finance/options/"
	url += ticker

	print(url)

	data = urlopen(url)
	data = json.loads(data.read().decode())
	for x in data['optionChain']['result']:
		for y in x['options']:
			for option in y['calls']:
				STRIKE_PRICE = option['strike']	        # S(T) price at maturity
				CURRENT_VALUE = option['lastPrice']
				VOLATILITY = option['impliedVolatility']
	for x in range(0,5):
		                                     # sigma i.e. volatility of underlying stock
		RISK_FREE_RATE = 1.1024                                 # mu
							# S(0) spot price, price of stock now

		# W(T) Wiener process/Brownian motion  = math.sqrt(T) * random.gauss(0, 1.0)

		NO_SIMULATIONS = 2

		START_DATE = datetime.date.today()
		EXPIRES = 55                                          # number of days until maturity date
		# european or asian call price
		def call_payoff(asset_price, STRIKE_PRICE): 
			return max(0.0, asset_price - STRIKE_PRICE)

		# simulate the option price
		def sim_option_price(seed, ): 
			random.seed(seed) 
			asset_price = CURRENT_VALUE * math.exp((RISK_FREE_RATE - .5 * VOLATILITY**2) * T + VOLATILITY * math.sqrt(T) * random.gauss(0,1.0)) 
			return call_payoff(asset_price, STRIKE_PRICE)

		# sequential approach, calculate option price every day until expiry
		option_prices = []
		times = []
		for i in range(1, EXPIRES + 1):                                                 # 1 .. EXPIRES inclusive
				sim_results = []                                                        # results from each simulation step
				T = i/365               # days in the future
				times.append(i)
				for j in range(NO_SIMULATIONS):
						sim_results.append(sim_option_price(time.time() + j))
				discount_factor = math.exp(-RISK_FREE_RATE * T)                         # e to the power of ()
				option_prices.append(discount_factor * (sum(sim_results) / float(NO_SIMULATIONS)))
				print (ticker," ","Option Price ", option_prices[i-1], " at ", START_DATE + datetime.timedelta(days=i))

		plt.plot(times, option_prices)
		plt.xlabel('T')
		plt.ylabel('Option Prices')
		#plt.show()

			