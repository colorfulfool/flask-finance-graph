from flask import Flask, Response, render_template

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

import yfinance as yf
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

def normalize(s):
    return (s - s.min()) / (s.max() - s.min())

def yahoo(ticker, start, end):
    data_frame = yf.download(ticker, start=start, end=end)
    if data_frame == None: raise RuntimeError("Couldn't load")
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
    return render_template("index.html")

@app.route("/plot.png")
def plot_png():
    yahoo = YahooFinance("2010-01-01", "2025-07-01")

    fig = Figure()
    plt = fig.add_subplot()
    plt.plot(yahoo.usd(), label='USD', color='green')
    plt.plot(yahoo.normalized('SPY'), label='S&P', color='red')
    plt.legend()
    plt.grid(True)

    byte_string = io.BytesIO()
    FigureCanvasAgg(fig).print_png(byte_string)
    return Response(byte_string.getvalue(), mimetype="image/png")
