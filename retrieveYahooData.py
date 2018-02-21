import json, datetime,urllib
from urllib.request import urlopen

def main(ticker):
    try:
        if "." in ticker:  # some tickers in list have "." when not needed
            ticker = ticker.replace(".", "")  # Removing "."
        url = createYahooUrlWithDate(ticker)
        data = urlopen(url)
        data = json.loads(data.read().decode())
        return data
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print("Page not found!")
        elif err.code == 403:
            print("Access denied!")
        else:
            print("Something happened! Error code", err.code)
    except urllib.error.URLError as err:
        print("Some other error happened:", err.reason)


def createYahooUrlWithDate(optionTicker):
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


# Stops code being run on import
if __name__ == "__main__":
	main()