from get_keys import *
import binance
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys

keys = get_keys()
api_key = keys[0]
api_secret = keys[1]

DEPART_SOMME = 1000

data_path = "/Users/raphaelfontaine/Documents/GIT/Trading/data/crossing_value.json"

def get_data():

    somme_investi = 0
    benef = 0
    pourcentage = 0

    # Créer une instance de client Binance
    client = binance.client.Client(api_key, api_secret)

    # Récupérer les données de cours par jour pour le Bitcoin
    klines = client.get_historical_klines("BTCUSDT", binance.client.Client.KLINE_INTERVAL_1DAY, "1 Jan, 2018", "16 Mar, 2023")

    # Convertir les données en dataframe pandas
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

    # Convertir en float le cours de cloture et d'ouverture
    df['close'] = df['close'].astype('float64')
    df['open'] = df['open'].astype('float64')

    # Convertir les timestamps en dates
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # Calculer la moyenne mobile exponentielle 200
    df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()

    operations = {}

    for i in range(200, len(df['ema_200']) - 1):
        if df['ema_200'][i] > df['close'][i] and (df['ema_200'][i] < df['close'][i+1] and df['ema_200'][i+1] < df['close'][i+2]):
            plt.annotate('BUY',
            ha = 'center', va = 'bottom',
            xytext = (df['timestamp'][i+1], df['ema_200'][i+1] + 5000),xy = (df['timestamp'][i+1], df['ema_200'][i+1]),arrowprops = {'facecolor' : 'green'})

            date = df['date'][i+1]
            dt = datetime.fromtimestamp(date.timestamp())
            date_str = dt.strftime('%Y-%m-%d')
            
            operations[date_str] = {}
            operations[date_str]['price'] = df['close'][i+1]
            operations[date_str]['achat'] = 0
            
        elif df['ema_200'][i] < df['close'][i] and (df['ema_200'][i] > df['close'][i+1] and df['ema_200'][i+1] > df['close'][i+2]):
            plt.annotate('SELL',
            ha = 'center', va = 'bottom',
            xytext = (df['timestamp'][i+1], df['ema_200'][i+1] + 5000),xy = (df['timestamp'][i+1], df['ema_200'][i+1]),arrowprops = {'facecolor' : 'red'})
            benef += df['close'][i+1]
            
            date = df['date'][i+1]
            dt = datetime.fromtimestamp(date.timestamp())
            date_str = dt.strftime('%Y-%m-%d')

            operations[date_str] = {}
            operations[date_str]['price'] = df['close'][i+1]
            operations[date_str]['achat'] = 1

    with open(data_path, 'w') as file:
        # Écrire une chaîne de caractères dans le fichier
        json.dump(operations, file, indent=4, sort_keys=True)

    plt.plot(df['timestamp'], df['close'])
    plt.plot(df['timestamp'], df['close'], color='r')
    plt.plot(df['timestamp'], df['ema_200'], color='g')
    plt.show()

def clean_json():
    with open(data_path, 'r') as f:
        operations_data = json.loads(f.read())
    dates = list(operations_data.keys())
    values = list(operations_data.values())

    first_op = values[0]["achat"]
    for k in range(1, len(dates)):
        operation = values[k]["achat"]
        if (operation == first_op):
            del operations_data[dates[k-1]]
        first_op = operation

    with open(data_path, 'w') as file:
        # Écrire une chaîne de caractères dans le fichier
        json.dump(operations_data, file, indent=4, sort_keys=True)


def profits_calcul(capital_start):
    with open(data_path, 'r') as f:
        operations_data = json.loads(f.read())
    dates = list(operations_data.keys())
    values = list(operations_data.values())

    rendement_total = 0
    nbr_operations = len(dates)
    for k in range(nbr_operations-1):
        achat = values[k]["achat"]
        price = values[k]["price"]
        next_price = values[k+1]["price"]       

        if(int(achat) == 0):
            rendement = (next_price - price)/price
            rendement_total += rendement
        elif(int(achat) == 1):
            rendement = (price - next_price)/price
            rendement_total += rendement
    print('RENDEMENT TOTAL : ', rendement_total*100,'%')
    

def main():
    # get_data()
    # clean_json()
    profits_calcul(DEPART_SOMME)


if __name__ == '__main__':
    sys.exit(main())