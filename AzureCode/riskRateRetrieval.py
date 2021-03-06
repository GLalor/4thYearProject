import quandl
import datetime
import json
from datetime import timedelta


def main():
    rates = []
    date = datetime.datetime.now().date() - timedelta(1)  # todays date
    mydata = quandl.get(
        "USTREASURY/YIELD",
        start_date=date,
        authtoken="ML7Kam1GdfzQ3Y4Ms-Ki")
    riskFreeRate = [mydata["3 MO"]]
    for i in range(
            1, 4):  # generates 4 risk free rates based of the Federal rate
        if i % 2 == 0:
            riskFreeRate.append(
                riskFreeRate[i - 1] + (riskFreeRate[i - 1] * (0.125 * i)))
        else:
            riskFreeRate.append(
                riskFreeRate[i - 1] - (riskFreeRate[i - 1] * (0.125 * i)))
    for rate in riskFreeRate:
        rates.append(float(rate[0]))
    return rates


# Stops code being run on import
if __name__ == "__main__":
    main()
