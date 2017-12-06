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

a = numpy.random.randn(1000,1) # 55x1 array of random numbers (set size to match experation)
a = a.astype(numpy.float32) # number format for card
a_gpu = cuda.mem_alloc(a.nbytes) # allocation of memory for card and cpu to use
cuda.memcpy_htod(a_gpu, a) # transfering the data to memeory location

# kernal code written in c
mod = SourceModule(""" 
    #include <stdio.h>
  __global__ void doublify(float *a, float strike, float current_value, float volatility, float risk_free_rate)
  {
    int idx = threadIdx.x;
    a[idx] = (current_value * (risk_free_rate - .5 * volatility * 2)  + volatility *  1.0);
  }
  """)
func = mod.get_function("doublify") #calling compiling function
# calc_start_time = time.time()

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
        for x in range(0, 10):
            func(a_gpu, numpy.float32(strike_price), numpy.float32(current_value), numpy.float32(volatility), numpy.float32(risk_free_rate), numpy.float32(T), block=(1000,1,1)) # passing arguments
            a_doubled = numpy.empty_like(a) 
            cuda.memcpy_dtoh(a_doubled, a_gpu) # retriving results
            option_prices.append(a_doubled)
            # print("******** GPU CALC finsihed in %s seconds ********" % (time.time() - calc_start_time))
# for i in option_prices:
#     print("Option Price ", i)
print("******** GPU finsihed in %s seconds ********" % (time.time() -start_time))