from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/tickers/<ticker>")
def show_ticker(ticker):
    return "Hello World!"+ ticker

if __name__ == "__main__":
    app.run()