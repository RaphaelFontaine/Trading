from binance.client import Client
import pandas as pd
import matplotlib.pyplot as plt
import ta

data = Client().get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "01 JANUARY 2018")
df = pd.DataFrame(data, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
somme_investi = 0
benef = 0

del df['ignore']
del df['close_time']
del df['quote_av']
del df['trades']
del df['tb_base_av']
del df['tb_quote_av']

df['close'] = pd.to_numeric(df['close'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['open'] = pd.to_numeric(df['open'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df['SMA50'] = ta.trend.sma_indicator(df['close'], 50)
df['SMA200'] = ta.trend.sma_indicator(df['close'], 200)

for i in range(len(df['SMA200']) - 1):
    if df['SMA200'][i] > df['SMA50'][i] and df['SMA200'][i+1] < df['SMA50'][i+1]:
        plt.annotate('BUY',
        ha = 'center', va = 'bottom',
        xytext = (df['timestamp'][i+1], df['SMA200'][i+1] + 5000),xy = (df['timestamp'][i+1], df['SMA200'][i+1]),arrowprops = {'facecolor' : 'green'})
        benef -= df['open'][i+1]
        somme_investi += df['open'][i+1]
        print("ACHAT: " + str(df['open'][i+1]) + " USDT")
    elif df['SMA200'][i] < df['SMA50'][i] and df['SMA200'][i+1] > df['SMA50'][i+1]:
        plt.annotate('SELL',
        ha = 'center', va = 'bottom',
        xytext = (df['timestamp'][i+1], df['SMA200'][i+1] + 5000),xy = (df['timestamp'][i+1], df['SMA200'][i+1]),arrowprops = {'facecolor' : 'red'})
        benef += df['open'][i+1]
        print("VENTE: " + str(df['open'][i+1]) + " USDT")

print("SOMME INVESTIE: " + str(somme_investi - benef))
print("BENEFICE TOTAL: " + str(benef))
plt.plot(df['timestamp'], df['open'])
plt.plot(df['timestamp'], df['SMA50'], color='r')
plt.plot(df['timestamp'], df['SMA200'], color='g')
plt.show()