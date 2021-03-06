import unittest
import optionCalculation
import optionCalculationSpark
import retrieveYahooData
import urllib
import json
import datetime
from urllib.request import urlopen

# Retrieve code coverage
# pip install coverage
# coverage run unitTest.py
# coverage report
# Name                                                                                   Stmts   Miss  Cover
# ----------------------------------------------------------------------------------------------------------
# optionCalculation.py                                                                      82     58    30%
# optionCalculationSpark.py                                                                 97     73    25%
# retrieveYahooData.py                                                                      39      9    81%
# writeToHDFS.py                                                                            10      4    60%                                                                           10      4    60%
# ----------------------------------------------------------------------------------------------------------
# coverage                                                                     (29 + 25 + 77 + 60) / 4 = 49%


class unitTestReadlist(unittest.TestCase):
    def test_call_payoff_negative(self):
        result = optionCalculation.call_payoff(20, 30)
        self.assertEqual(0.0, result)

    def test_call_payoff_positive(self):
        result = optionCalculation.call_payoff(60, 50)
        self.assertEqual(10.0, result)

    def test_put_payoff_negative(self):
        result = optionCalculation.put_payoff(30, 20)
        self.assertEqual(0.0, result)

    def test_put_payoff_positive(self):
        result = optionCalculation.put_payoff(50, 60)
        self.assertEqual(10.0, result)

    def test_sim_option_price_call(self):
        result = optionCalculation.sim_option_price(
            1, 50, 2.1024, .367, 70, 77, "Call")
        self.assertEqual(1.9218778063361091e+65, result)

    def test_sim_option_price_put(self):
        result = optionCalculation.sim_option_price(
            1, 50, 2.1024, .367, 70, 77, "Put")
        self.assertEqual(0.0, result)

    def test_call_payoff_spark_negative(self):
        result = optionCalculationSpark.call_payoff(50, 70)
        self.assertEqual(0.0, result)

    def test_put_payoff_spark_negative(self):
        result = optionCalculationSpark.put_payoff(10, 5)
        self.assertEqual(0.0, result)

    def test_call_payoff_spark_positive(self):
        result = optionCalculationSpark.call_payoff(6, 3)
        self.assertEqual(3.0, result)

    def test_put_payoff_spark_positive(self):
        result = optionCalculationSpark.put_payoff(100, 120)
        self.assertEqual(20.0, result)


    def test_sim_option_price_call_spark(self):
        result = optionCalculationSpark.sim_option_price(
            1, 50, 2.1024, .367, 70, 77, "Call")
        self.assertEqual(1.9218778063361091e+65, result)

    def test_sim_option_price_put_spark(self):
        result = optionCalculationSpark.sim_option_price(
            1, 50, 2.1024, .367, 70, 77, "Put")
        self.assertEqual(0.0, result)

    def test_createYahooUrl_valid_ticker(self):
        result = retrieveYahooData.createYahooUrlWithDate("MMM")
        # Retrieves latest date for test
        url = "https://query2.finance.yahoo.com/v7/finance/options/MMM"
        data = urlopen(url)
        data = json.loads(data.read().decode())
        expirationDates = data['optionChain']['result'][0]['expirationDates']
        for item in expirationDates:
            dt = datetime.datetime.fromtimestamp(
                item) - datetime.datetime.now()
            if dt.days > 0:
                expDate = str(item)
                break
        self.assertEqual(
            "https://query2.finance.yahoo.com/v7/finance/options/MMM?date=" +
            expDate,
            result)

    def test_createYahooUrl_invalid_ticker(self):
        self.assertRaises(urllib.error.HTTPError,
                          retrieveYahooData.createYahooUrlWithDate, "x12")

    def test_createYahooUrl_invalid_data(self):
        result = retrieveYahooData.main('156')
        self.assertEqual(False, result)

    def test_fullstop_removal(self):
        data = urlopen(
            "https://query2.finance.yahoo.com/v7/finance/options/BFB")
        data = json.loads(data.read().decode())
        # BFB doesnt always have options and return false if expiration date is
        # empty so set to false to confirm this
        if not data['optionChain']['result'][0]['expirationDates']:
            data = False
        ticker = "BF.B"
        result = retrieveYahooData.main(ticker)
        self.assertEqual(data, result)


if __name__ == '__main__':
    unittest.main()
