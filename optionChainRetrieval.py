import json, datetime, random, math, time
from urllib.request import urlopen
#from operator import add
#import matplotlib.pyplot as plt  # mathplotlib

def main(ticker):
		option_type = "not set"
		strike_price = 0        # S(T) price at maturity
		current_value = 0		# S(0) spot price, price of stock now
		volatility = .3672 			# sigma i.e. volatility of underlying stock
		risk_free_rate = 2.1024  # mu
		expires = 55  # Number of days until maturity date
		if "." in ticker:  # some tickers in list have "." when not needed
			ticker = ticker.replace(".", "")  # Removing "."
		url = "https://query2.finance.yahoo.com/v7/finance/options/"
		url += ticker+"?date=1513900800"

		print(url)  # Prints URL to option chain
		
		data = urlopen(url)
		data = json.loads(data.read().decode())
		for item in data['optionChain']['result']:
			current_value = item['quote']['regularMarketPrice']
			data = item['options']
		for option in data:
			calls, puts = option['calls'], option['puts']
			
		for call in calls:
			print("call")
			option_type = "Call"
			strike_price = call['strike']	        # S(T) price at maturity
			volatility = call['impliedVolatility']
			dt = datetime.datetime.fromtimestamp(call['expiration']) - datetime.datetime.now()
			expires = dt.days
			runSimulaion(option_type, strike_price, current_value,
							volatility, risk_free_rate, expires, ticker)



def runSimulaion(option_type, strike_price, current_value, volatility, risk_free_rate, expires, ticker):
	start_date = datetime.date.today()
	num_simulations = 10000
	for x in range(0, 5):
		# W(T) Wiener process/Brownian motion  = math.sqrt(T) * random.gauss(0, 1.0)
		# sequential approach, calculate option price every day until expiry
		option_prices = []
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
			# print(ticker, " ", option_type, " ", "Option Price ",
			# 	option_prices[i - 1], " at ", start_date + datetime.timedelta(days=i))
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

# Stops code being run on import
if __name__ == "__main__":
	main()




import pycuda.autoinit, json, datetime, random, math, time
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from urllib.request import urlopen
import numpy

ticker = "AAPL"
start_time = time.time()
num_simulations = 10000      
option_type = "not set"    
strike_price = 120.0        # S(T) price at maturity
current_value = 49.8		# S(0) spot price, price of stock now
volatility = 1.6015644921874999 			# sigma i.e. volatility of underlying stock
risk_free_rate = 2.1024  # mu
expires = 55  # Number of days until maturity date
option_prices = []


# kernal code written in c
mod = SourceModule(""" 
#include <stdio.h>
  __global__ void doublify(float *sim_results, float strike, float current_value, float volatility, float risk_free_rate, int T, int expires, int num_simulations)
  {
    //int idx = threadIdx.x + threadIdx.y*expires;
    for(int i = 0; i <= 10000; i++){
        sim_results[i] = (current_value * (risk_free_rate - .5 * volatility * 2) * T + volatility * (T) * 1.0);
    }
  }
  """)
func = mod.get_function("doublify") #calling compiling function


if "." in ticker:  # some tickers in list have "." when not needed
    ticker = ticker.replace(".", "")  # Removing "."
url = "https://query2.finance.yahoo.com/v7/finance/options/"
url += ticker+"?date=1513900800"

print(url)  # Prints URL to option chain

data = urlopen(url)
data = json.loads(data.read().decode())
for item in data['optionChain']['result']:
    current_value = item['quote']['regularMarketPrice']
    data = item['options']
for option in data:
    calls, puts = option['calls'], option['puts']
    
for call in calls:
    option_type = "Call"
    strike_price = call['strike']	        # S(T) price at maturity
    volatility = call['impliedVolatility']
    dt = datetime.datetime.fromtimestamp(call['expiration']) - datetime.datetime.now()
    expires = dt.days
    for j in range(expires): # Monte carlo Sim 10'000
        T = j/365
        discount_factor = math.exp(-risk_free_rate * T)
        #sim_results = numpy.zeros(num_simulations)

        # PYCUDA
        a = numpy.zeros(num_simulations) # array (set size to match experation)
        a = a.astype(numpy.float32) # number format for card
        a_gpu = cuda.mem_alloc(a.nbytes) # allocation of memory for card and cpu to use
        cuda.memcpy_htod(a_gpu, a) # transfering the data to memeory location

        func(a_gpu, numpy.float32(strike_price), numpy.float32(current_value), numpy.float32(volatility), numpy.float32(risk_free_rate), numpy.uint32(T), numpy.uint32(expires), numpy.uint32(num_simulations), block=(expires,1,1)) # passing arguments
        a_doubled = numpy.empty_like(a) 
        cuda.memcpy_dtoh(a_doubled, a_gpu) # retriving results

        #option_prices.append(discount_factor * (sum(sim_results) / float(num_simulations)))

    for i in a:
        print("Option Price ", i)
print("******** GPU finsihed in %s seconds ********" % (time.time() -start_time))