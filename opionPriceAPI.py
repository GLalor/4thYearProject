import json
from flask import Flask, jsonify, abort

app = Flask(__name__)

data = json.load(open('optionPrices.json'))

@app.route("/")
def optionList():
    return jsonify(data)

@app.route("/tickerData/<ticker>")
def tickerData(ticker):
    if ticker in data:
        return jsonify(data[ticker])
    else:
         return abort(404)   

@app.route("/bestPrice/<ticker>/<optionType>")
def tickerPrices(ticker, optionType):
    maxPrice = 0
    date = ""
    if ticker in data and optionType in data[ticker]:
        for item in data[ticker][optionType]:
            if data[ticker][optionType][item] > maxPrice:
                maxPrice = data[ticker][optionType][item]
                date = item
        return "The best " + optionType + " option price for " + ticker +" is " + "{:.2f}".format(maxPrice) + " on " + date
    else:
         return abort(404)

if __name__ == "__main__":
    app.run()