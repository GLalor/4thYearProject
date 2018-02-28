import pycuda.autoinit, json, datetime, random, math, time, urllib, retrieveYahooData,writeToHDFS
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from urllib.request import urlopen
import numpy


option_prices = {}

def main(ticker, riskFreeRates):
    #ticker = "BCR"
    start_time = time.time()
    num_simulations = 10000      
    option_type = "not set"    
    strike_price = 120.0        # S(T) price at maturity
    current_value = 49.8		# S(0) spot price, price of stock now
    volatility = 1.6015644921874999 			# sigma i.e. volatility of underlying stock
    expires = 55  # Number of days until maturity date
    risk_free_rate = riskFreeRates # risk free rate from fed
    start_date = datetime.date.today()
    riskResults = {}
    priceResults = []
    call_results = {}
    put_results = {}

    a = numpy.random.randn(1000) # 55x1 array of random numbers (set size to match experation)
    a = a.astype(numpy.float32) # number format for card
    a_gpu = cuda.mem_alloc(a.nbytes) # allocation of memory for card and cpu to use
    cuda.memcpy_htod(a_gpu, a) # transfering the data to memeory location

    # kernal code written in c
    mod = SourceModule(""" 
        #include <math.h>
    __global__ void doublify(float *a, float strike, float current_value, float volatility, float risk_free_rate, float T, float randNum)
    {
        int idx = threadIdx.x;
        a[idx] = exp(current_value * (risk_free_rate - .5 * pow(volatility,2)) * T + volatility * sqrt(T) * randNum);
    }
    """)
    func = mod.get_function("doublify") #calling compiling function
    # calc_start_time = time.time()
    data = retrieveYahooData.main(ticker)
    if data is not None and data is not False:
        option_prices['Ticker'] = ticker
        option_prices['Risk Free Rates'] = risk_free_rate
    
        if "regularMarketPrice" in data['optionChain']['result'][0]['quote']:
            current_value = data['optionChain']['result'][0]['quote']['regularMarketPrice']
            data = data['optionChain']['result'][0]['options']
            for option in data:
                calls, puts = option['calls'], option['puts']
                
            for call in calls:
                option_type = "Call"
                strike_price = call['strike'] # S(T) price at maturity
                riskResults['Strike Price'] = strike_price     
                volatility = call['impliedVolatility']
                riskResults['Volatility'] = volatility
                dt = datetime.datetime.fromtimestamp(call['expiration']) - datetime.datetime.now()
                expires = dt.days
                option_prices['Number of Days'] = expires
                option_prices['ExpirationDate'] = datetime.datetime.fromtimestamp(
                call['expiration']).strftime('%Y-%m-%d')
                for rate in risk_free_rate:
                    riskResults['RiskFreeRate'] = rate
                    for j in range(1, expires + 1): # Monte carlo Sim 10'000
                        sim_results = []
                        sim_prices = []
                        
                        sim_results_total = 0
                        T = j/365
                    
                        discount_factor = math.exp(-rate * T)
                        for x in range(0, 10):
                            func(a_gpu, numpy.float32(strike_price), numpy.float32(current_value), numpy.float32(volatility), numpy.float32(rate), numpy.float32(T), numpy.float32(random.gauss(0, 1.0)), block=(1000,1,1)) # passing arguments
                            a_doubled = numpy.empty_like(a) 
                            cuda.memcpy_dtoh(a_doubled, a_gpu) # retriving results
                            sim_results.append(a_doubled)
                            for x in range(1000):
                                sim_results[0][x] = max(0.0, sim_results[0][x] - strike_price)
                                sim_results_total += sim_results[0][x]
                        sim_prices.append(discount_factor * (sim_results_total / float(num_simulations)))
                        for x in sim_prices:
                            call_results[(str(start_date + datetime.timedelta(days=j)))] = (float(x))
                    riskResults[option_type] = call_results
                    priceResults.append(riskResults.copy())
            # option_prices['prices'] = priceResults
            riskResults = {} # reset riskResults dicionary 
            for put in puts:
                option_type = "Put"
                strike_price = put['strike']	        # S(T) price at maturity
                riskResults['Strike Price'] = strike_price 
                volatility = put['impliedVolatility']
                riskResults['Volatility'] = volatility
                dt = datetime.datetime.fromtimestamp(put['expiration']) - datetime.datetime.now()
                expires = dt.days
                option_prices['Number of Days'] = expires
                for rate in risk_free_rate:
                    riskResults['RiskFreeRate'] = rate
                    for j in range(1, expires + 1): # Monte carlo Sim 10'000
                        sim_results = []
                        sim_prices = []
                        
                        sim_results_total = 0
                        T = j/365
                        
                        discount_factor = math.exp(-rate * T)
                        for x in range(0, 10):
                            func(a_gpu, numpy.float32(strike_price), numpy.float32(current_value), numpy.float32(volatility), numpy.float32(rate), numpy.float32(T), numpy.float32(random.gauss(0, 1.0)), block=(1000,1,1)) # passing arguments
                            a_doubled = numpy.empty_like(a) 
                            cuda.memcpy_dtoh(a_doubled, a_gpu) # retriving results
                            sim_results.append(a_doubled)
                            for x in range(1000):
                                sim_results[0][x] = max(0.0, strike_price - sim_results[0][x])
                                sim_results_total += sim_results[0][x]
                        sim_prices.append(discount_factor * (sim_results_total / float(num_simulations)))
                        for x in sim_prices:
                            put_results[(str(start_date + datetime.timedelta(days=j)))] = (float(x))
                    riskResults[option_type] = put_results
                    priceResults.append(riskResults)

            option_prices['Prices'] = priceResults

    else:
        call_results['NA'] = "MISSING DATA"
        put_results['NA'] = "MISSING DATA"
        riskResults[option_type] = call_results
        riskResults[option_type] = put_results
        option_prices['Prices'] = priceResults
    
    with open('optionPrices.json', 'w') as outfile:
            json.dump(option_prices,outfile)
    writeToHDFS.writeResultHive()
    print("******** GPU finished in %s seconds ********" % (time.time() -start_time))