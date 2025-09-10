from flask import Flask, Response, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

import yfinance as yf
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

def normalize(s):
    return (s / s.iloc[0])

def yahoo(ticker, start, end):
    data_frame = yf.download(ticker, start=start, end=end)
    return data_frame['Close', ticker]

class YahooFinance:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.gold = self.ticker("GC=F")

    def ticker(self, ticker):
        return yahoo(ticker, self.start, self.end)

    def usd(self):
        return normalize(1 / self.gold)

    def normalized(self, ticker):
        return normalize(self.ticker(ticker) / self.gold)

@app.route("/")
def hello_world():
    start, end = "2010-01-01", "2025-07-01"
    return render_template("index.html", start=start, end=end)

@app.route("/plot.png")
def plot_png():
    yahoo = YahooFinance(request.args.get("start"), request.args.get("end"))

    fig = Figure()
    plt = fig.add_subplot()
    plt.plot(yahoo.usd(), label='USD', color='green')
    plt.plot(yahoo.normalized('SPY'), label='S&P', color='red')
    plt.plot(yahoo.normalized('CHFUSD=X'), label='CHF', color='blue')
    plt.plot(yahoo.normalized('KZTUSD=X'), label='KZT', color='turquoise')
    plt.legend()
    plt.autoscale(tight=True)
    plt.grid(True)

    byte_string = io.BytesIO()
    FigureCanvasAgg(fig).print_png(byte_string)
    return Response(byte_string.getvalue(), mimetype="image/png")
