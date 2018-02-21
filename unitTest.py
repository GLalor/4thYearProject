import unittest, optionCalculation, retrieveYahooData
import urllib, json, datetime
from urllib.request import urlopen

# Retrieve code coverage
# pip install coverage
# coverage run unitTest.py
# coverage report (focus on first 2 lines)
# coverage report
#  Name                                                                                   Stmts   Miss  Cover
#  ----------------------------------------------------------------------------------------------------------
#  optionCalculation.py                                                                      73     55    25%
#  retrieveYahooData.py                                                                      31     16    48%
#  writeToHDFS.py                                                                            10      4    60%

class unitTestReadlist(unittest.TestCase):
    def test_call_payoff(self):
        result = optionCalculation.call_payoff(20,20)
        self.assertEqual(0.0 , result)

    def test_put_payoff(self):
        result = optionCalculation.put_payoff(20,20)
        self.assertEqual(0.0 , result)
    
    def test_sim_option_price_call(self):
        result = optionCalculation.sim_option_price(1,50,2.1024,.367,70,77,"Call")
        self.assertEqual(1.9218778063361091e+65 , result)

    def test_sim_option_price_put(self):
        result = optionCalculation.sim_option_price(1,50,2.1024,.367,70,77,"Put")
        self.assertEqual(0.0 , result)

    def test_createYahooUrl_valid_ticker(self):
        result = retrieveYahooData.createYahooUrlWithDate("MMM")
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
        self.assertRaises(urllib.error.HTTPError, retrieveYahooData.createYahooUrlWithDate, "x12")

if __name__ == '__main__':
    unittest.main()