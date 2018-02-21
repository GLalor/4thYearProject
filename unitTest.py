import unittest
import optionChainRetrieval
import urllib, json, datetime
from urllib.request import urlopen
# code coverage = 45% - optionChainRetrieval
# Retrieve code coverage
# pip install coverage
# coverage run unitTest.py
# coverage report (focus on first 2 lines)

class unitTestReadlist(unittest.TestCase):
    def test_call_payoff(self):
        result = optionChainRetrieval.call_payoff(20,20)
        self.assertEqual(0.0 , result)

    def test_put_payoff(self):
        result = optionChainRetrieval.put_payoff(20,20)
        self.assertEqual(0.0 , result)
    
    def test_sim_option_price_call(self):
        result = optionChainRetrieval.sim_option_price(1,50,2.1024,.367,70,77,"Call")
        self.assertEqual(1.9218778063361091e+65 , result)

    def test_sim_option_price_put(self):
        result = optionChainRetrieval.sim_option_price(1,50,2.1024,.367,70,77,"Put")
        self.assertEqual(0.0 , result)

    def test_main_invalid_ticker(self):
        self.assertRaises(AttributeError, optionChainRetrieval.main, "x12")
    
    def test_createYahooUrl_valid_ticker(self):
        result = optionChainRetrieval.createYahooUrl("MMM")
        # Retrieves latest date for test
        url = "https://query2.finance.yahoo.com/v7/finance/options/MMM"
        data = urlopen(url)
        data = json.loads(data.read().decode())
        expirationDates = data['optionChain']['result'][0]['expirationDates']
        for item in expirationDates:
            dt = datetime.datetime.fromtimestamp(item) - datetime.datetime.now()
            if dt.days > 0:
                expDate = str(item)
                break
        self.assertEqual( "https://query2.finance.yahoo.com/v7/finance/options/MMM?date="+expDate, result)
    
    def test_createYahooUrl_invalid_ticker(self):
        self.assertRaises(AttributeError, optionChainRetrieval.main, "x12")

if __name__ == '__main__':
    unittest.main()