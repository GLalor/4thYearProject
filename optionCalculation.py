import json
import datetime
import random
import math
import time
import retrieveYahooData
import writeToHDFS
#from operator import add
# import matplotlib.pyplot as plt  # mathplotlib

# Dictionaries for json output
option_prices = {}
results = {}
call_results = {}
put_results = {}


def main(ticker):
	option_type = "not set"
	strike_price = 0        # S(T) price at maturity
	current_value = 0           # S(0) spot price, price of stock now
	volatility = .3672                  # sigma i.e. volatility of underlying stock
	risk_free_rate = 2.1024  # mu
	expires = 55  # Number of days until maturity date

	data = retrieveYahooData.main(ticker)
	option_prices['Ticker'] = ticker
	# Cutting down on loops

	#data['optionChain']['result'][0]['expirationDates']
	# Test if is regularMarketPrice present will move to check if date is present in experationDates when working with dates
	if "regularMarketPrice" in data['optionChain']['result'][0]['quote']:
		current_value = data['optionChain']['result'][0]['quote']['regularMarketPrice']
		data = data['optionChain']['result'][0]['options']
		for option in data:
			calls, puts = option['calls'], option['puts']
		# Assigning variables for calc and running sim
		for call in calls:
			option_type = "Call"
			strike_price = call['strike']           # S(T) price at maturity
			volatility = call['impliedVolatility']
			dt = datetime.datetime.fromtimestamp(
			call['expiration']) - datetime.datetime.now()
			expires = dt.days
			option_prices['ExpirationDate'] = datetime.datetime.fromtimestamp(
			call['expiration']).strftime('%Y-%m-%d')
			runSimulaion(option_type, strike_price, current_value,
							volatility, risk_free_rate, expires, ticker)
			results[option_type] = call_results
		for put in puts:
			option_type = "Put"
			strike_price = put['strike']            # S(T) price at maturity
			volatility = put['impliedVolatility']
			runSimulaion(option_type, strike_price, current_value,
							volatility, risk_free_rate, expires, ticker)
			results[option_type] = put_results
			option_prices['Prices'] = results
	else:
		call_results['NA'] = "MISSING DATA"
		put_results['NA'] = "MISSING DATA"
		results[option_type] = call_results
		results[option_type] = put_results
		option_prices['Prices'] = results

	with open('optionPrices.json', 'w') as outfile:
		json.dump(option_prices, outfile)
	writeToHDFS.writeResultHive()


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
                call_results[(
                    str(start_date + datetime.timedelta(days=i)))] = option_prices
                # print(ticker, " ", option_type, " ", "Option Price ",
                # option_prices[i - 1], " at ", start_date + datetime.timedelta(days=i))
            else:
                put_results[(
                    str(start_date + datetime.timedelta(days=i)))] = option_prices
                # print(ticker, " ", option_type, " ", "Option Price ",
                # option_prices[i - 1], " at ", start_date + datetime.timedelta(days=i))

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