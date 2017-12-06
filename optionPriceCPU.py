import json, datetime, random, math, time
from urllib.request import urlopen
import numpy as np

ticker = "AAPL"
start_time = time.time()
num_simulations = 10000    
strike_price = 120.0        # S(T) price at maturity
current_value = 49.8		# S(0) spot price, price of stock now
volatility = 1.6015644921874999 			# sigma i.e. volatility of underlying stock
risk_free_rate = 2.1024  # mu
expires = 55  # Number of days until maturity date
a = np.zeros(55)

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
    for i in range(expires):
        for j in range(num_simulations): # Monte carlo Sim 10'000
            T = i/365
            a[i] = (current_value * (risk_free_rate - .5 * volatility * 2) * T + volatility * (T) * 1.0)
        # for i in a:
        #     print(" Option Price ", i)

print("******** CPU finsihed in %s seconds ********" % (time.time() -start_time))