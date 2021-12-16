import pickle
from tqdm import tqdm
from datetime import timedelta, datetime
import math
import sys
import pandas as pd
import json
import requests


if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Usage: coinbaseExplorer2.py symbol-name kline-size start-timestamp end-timestamp")
        sys.exit(1)

    products_response = requests.get("https://api.pro.coinbase.com/products")
    norm_product_response = pd.json_normalize(json.loads(products_response.text))
    cb_ticker_list = norm_product_response['id'].tolist()

    time_format = "%Y-%m-%d %H:%M:%S"
    batch_size = 300
    binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}

    ticker = sys.argv[1]
    kline_size = sys.argv[2]
    start_time_string = sys.argv[3]
    start_time = datetime.strptime(start_time_string, time_format)
    end_time_string = sys.argv[4]
    end_time = datetime.strptime(end_time_string, time_format)

    if ticker not in cb_ticker_list:
        print("Ticker not supported by coinbase")
        sys.exit(1)

    minute_timespan = (end_time - start_time).total_seconds()/60
    num_datapoints = math.ceil(minute_timespan/binsizes[kline_size])
    num_queries = math.ceil(num_datapoints/batch_size)

    data = pd.DataFrame()
    close_list = []
    open_list = []
    high_list = []
    low_list = []
    timestamp_list = []

    for query_iter in tqdm(range(num_queries)):
        temp_start_time = start_time + timedelta(minutes = query_iter * batch_size * binsizes[kline_size])
        temp_end_time = temp_start_time + timedelta(minutes = (batch_size-1) * binsizes[kline_size])
        temp_response = requests.get("https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}" \
                                     .format(ticker, temp_start_time, temp_end_time, kline_size))
        temp_response_df = pd.DataFrame(json.loads(temp_response.text))
        temp_response_df[0] = pd.to_datetime(temp_response_df[0], unit='s')
        data = data.append(temp_response_df)
        close_list.append(temp_response_df[4].tolist())
        open_list.append(temp_response_df[3].tolist())
        low_list.append(temp_response_df[1].tolist())
        high_list.append(temp_response_df[2].tolist())
        timestamp_list.append(temp_response_df[0].tolist())

    data.columns = ["time", "low", "high", "open", "close", "volume"]

    stored_vars={}
    stored_vars["timestamp_list"] = timestamp_list
    stored_vars["close_list"] = close_list
    stored_vars["open_list"] = open_list
    stored_vars["high_list"] = high_list
    stored_vars["low_list"] = low_list

    with open('data/coinbase_' + ticker + '_' + kline_size + '_' + start_time_string + '_' + end_time_string + '_list.pickle','wb') as handle:
        pickle.dump(stored_vars, handle, protocol = pickle.HIGHEST_PROTOCOL)
    data.to_pickle('data/coinbase_pandas_' + ticker + '_' + kline_size + '_' + start_time_string + '_' + end_time_string + '_list.pickle')