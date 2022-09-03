import time
import pandas as pd  # to create a stock data frame
from datetime import date, timedelta  # for start and end periods
import uuid  # to generate random id

print(date.today())


class YahooAPI(object):

    def __init__(self, interval="1d"):
        self.base_url = "https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_time}&period2={" \
                        "end_time}&interval={interval}&events=history "
        self.interval = interval

    def __build_url(self, ticker, start_date, end_date):
        return self.base_url.format(ticker=ticker, start_time=start_date, end_time=end_date, interval=self.interval)

    def get_ticker_data(self, ticker, start_date, end_date):
        epoch_start = int(time.mktime(start_date.timetuple()))
        epoch_end = int(time.mktime(end_date.timetuple()))
        return pd.read_csv(self.__build_url(ticker, epoch_start, epoch_end))


if __name__ == '__main__':
    dh = YahooAPI()
    with open("ticker_symbols.txt", "r") as f:
        tickers = [(line.strip()).split() for line in f]
    print(tickers)
    for ticker in tickers:
        try:
            print(str(ticker[0]))
            df = dh.get_ticker_data(str(ticker[0]), date.today() - timedelta(days=8), date.today())
            df = df.drop(['Adj Close'], axis=1)
            df = df.drop(['Volume'], axis=1)
            df['Date'] = pd.to_datetime(df['Date'])
            df['ticker_symbol'] = str(ticker[0])
            df['high_diff'] = (df.High.diff() / df.High * 100).round(2)
            df['id'] = str(uuid.uuid1())
            print(df)
            csv_data = df.to_csv('data/' + str(ticker[0]) + '.csv')
            # print(df.dtypes)


        except:
            print("No information for ticker: " + str(ticker[0]))
            continue
