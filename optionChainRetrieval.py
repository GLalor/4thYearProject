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
			print(ticker, " ", option_type, " ", "Option Price ",
				option_prices[i - 1], " at ", start_date + datetime.timedelta(days=i))
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
