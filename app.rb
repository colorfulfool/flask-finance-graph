class YahooFetcher
  def initialize
    @cookie = fetch_cookie "https://fc.yahoo.com"
    @crumb = fetch_text "https://query1.finance.yahoo.com/v1/test/getcrumb"
  end

  def fetch_ticker(name)
    data = fetch_json "https://query1.finance.yahoo.com/v7/finance/download?symbols=#{name}&crumb=#{@crumb}"
  end

  private

    def fetch_cookie(url)

    end
end

class YahooProvider
  def initialize(start, end)
    @start = start
    @end = end
  end

  def yahoo_fetcher
    @yahoo_fetcher ||= new YahooFetcher
  end

  def gold
    @gold ||= ticker("GC=F")
  end

  def ticker(name)
    yahoo_fetcher.fetch_ticker(name, @start, @end)    
  end
end

yahoo = new YahooProvider(start, end)

plot do |line|
  line "USD", "green", normalize(1 / yahoo.gold)
  line "S&P", "red", normalize(yahoo.ticker("SPY") / yahoo.gold)
  line "CHF", "blue", normalize(yahoo.ticker("CHFUSD=X") / yahoo.gold)
  line "KZT", "turquoise", normalize(yahoo.ticker("KZTUSD=X") / yahoo.gold)
end
