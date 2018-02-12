import requests
import datetime
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.callbacks import EarlyStopping

import pybitflyer



def get_now_price(symbol="BTC", comparison_symbols=['JPY'], exchange=''):
    """
    BTC-JPYの現在価格
    :param symbol: 　買いたいもの
    :param comparison_symbols: 　売りたいもの　
    :param exchange:
    :return:
    """
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'.format(symbol.upper(),
                                                                                 ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    return data


def get_minutely_price(symbol, comparison_symbol, limit, aggregate,exchange=''):
    """
    一分足で現在～過去データ取得
    :param symbol:
    :param comparison_symbol:
    :param limit:
    :param aggregate:
    :param exchange:
    :return:
    """
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'.format(symbol.upper(),
                                                                                                            comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


def get_minutely_price_before(symbol, comparison_symbol, limit,aggregate,time,exchange=''):
    """
    過去～過去の一分足データを取得
    :param symbol:
    :param comparison_symbol:
    :param limit:
    :param aggregate:
    :param time:
    :param exchange:
    :return:
    """
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}&toTs={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate,time)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

"""
過去一週間のデータを取得
"""
coin_data = get_minutely_price('BTC', 'JPY', 1440, 1)
for i in range(0, 6):
    last_time = coin_data.time[0]-60
    price_data_before = get_minutely_price_before('BTC', 'JPY', 1440, 1, last_time)
    coin_data = pd.concat([price_data_before, coin_data], ignore_index=True)


"""
データの標準化
"""
price_data = pd.DataFrame([float(price) for price in coin_data.close])
ss = StandardScaler()
input_price = pd.DataFrame(ss.fit_transform(price_data))


def _load_data(data, time_step=60):
    """
    データを分割
    :param data:
    :param time_step:
    :return:
    """
    price_window, prices = [], []
    for p in range(len(data)-time_step):
        price_window.append(data.iloc[p:p+time_step].as_matrix())
        prices.append(data.iloc[p+time_step].as_matrix())
    arr_x = np.array(price_window)
    arr_y = np.array(prices)
    return (arr_x, arr_y)


def create_data(data, time_step=60):
    X= []
    for i in range(len(data)-time_step+1):
        X.append(data.iloc[i:i+time_step].as_matrix())
    arrayX = np.array(X)

    return arrayX


def train_test_split(df, test_size=0.1, time_step=60):
    """
    訓練データとテストデータに分割
    :param df:
    :param test_size:
    :param time_step:
    :return:
    """
    train_len = round(len(df) * (1 - test_size))
    train_len = int(train_len)
    X_train, y_train = _load_data(df[0:train_len], time_step)
    X_test, y_test = _load_data(df[train_len:-1], time_step)
    return (X_train, y_train), (X_test, y_test)


(X_train, y_train), (X_test, y_test) = train_test_split(input_price)
"""
バッチサイズで割り切るためにデータ数を調整
"""
X_train = X_train[12:]
y_train = y_train[12:]
X_test = X_test[:900]
y_test = y_test[:900]


"""
モデルの構築
LSTM二層、全結合層
"""

in_out_neurons = 1
hidden_neurons = 300
time_step = 60
batch_size = 300


model = Sequential()
model.add(LSTM(hidden_neurons, batch_input_shape=(batch_size, time_step, in_out_neurons),return_sequences=True))
model.add(LSTM(hidden_neurons, batch_input_shape=(batch_size, time_step, in_out_neurons),return_sequences=False))
model.add(Dense(in_out_neurons))
model.add(Activation("linear"))
model.compile(loss="mean_squared_error", optimizer="adam")


"""
モデルの学習
"""
early_stopping = EarlyStopping(monitor='loss', mode='auto', patience=0)
for i in range(50):
    model.fit(X_train, y_train, epochs=1, batch_size=batch_size,
              verbose=2, shuffle=False, callbacks=[early_stopping])
    model.reset_states()


"""
一分足で一時間先で予測
"""
real_price = get_minutely_price('BTC', 'JPY', 358, 1)
real_data = pd.DataFrame([float(price) for price in real_price.close])
real_input = pd.DataFrame(ss.fit_transform(real_data))
future_prices = []

for i in range(60):
    real_X = create_data(real_input)
    predicted_data = model.predict(real_X, batch_size)
    future_prices.append(predicted_data[-1])
    real_input = pd.concat([real_input, pd.DataFrame(predicted_data[-1])], ignore_index=True)
    real_input = real_input[1:]


"""
自動注文
while文とsleep()で一時間ごとに予測、注文を出す、、、予定
"""
public_api = pybitflyer.API()
api = pybitflyer.API(api_key="[YOUR API_KEY]", api_secret="[YOUR API SERCRET]")

"""
注文
"""


def order(order_type, side, size):
    size = 0.001*size
    api.sendchildorder(product_code="BTC_JPY", child_order_type=order_type
                       , side=side, size=size)
