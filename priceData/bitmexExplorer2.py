import pickle
import time
from tqdm import tqdm
from bitmex import bitmex
from datetime import timedelta,datetime
import math
import sys
import pandas as pd
import json

if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Usage: bitmexExplorer2.py symbol-name kline-size start-timestamp end-timestamp")
        sys.exit(1)

    bitmex_api_key = '1JnAJmntWdiOeYpv2bCJIGCj'    #Testnet API keys
    bitmex_api_secret = '5TE3OhqDTCl6ffrCCug-XwA0mINL-1tSiBbctXIfozHqFkYX'

    binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
    batch_size = 500
    bitmex_client = bitmex(test=True, api_key=bitmex_api_key, api_secret=bitmex_api_secret) #Fetching from bitmex testnet

    default_symbol = sys.argv[1]
    default_kline_size = sys.argv[2]
    start_timestamp = sys.argv[3]
    time_format = "%Y-%m-%d %H:%M:%S"
    # If no start timestamp is specified, start from the listing date on bitmex
    if start_timestamp=="None":
        start_timestamp = bitmex_client.Trade.Trade_getBucketed(symbol=default_symbol, \
                                    binSize=default_kline_size, count=1, reverse=False).result()[0][0]['timestamp']
    else:
        start_timestamp = datetime.strptime(start_timestamp, time_format)
    end_timestamp = sys.argv[4]
    # If no start timestamp is specified, end at latest data point available (reverse=True)
    if end_timestamp=="None":
        end_timestamp = bitmex_client.Trade.Trade_getBucketed(symbol=default_symbol, \
                                    binSize=default_kline_size, count=1, reverse=True).result()[0][0]['timestamp']
    else:
        end_timestamp = datetime.strptime(end_timestamp, time_format)
    minute_timespan = (end_timestamp - start_timestamp).total_seconds()/60
    num_datapoints = math.ceil(minute_timespan/binsizes[default_kline_size])
    num_queries = math.ceil(num_datapoints/batch_size)
    close_list = []
    open_list = []
    high_list = []
    low_list = []
    timestamp_list = []

    for query_iter in tqdm(range(num_queries)):
        new_start_timestamp = start_timestamp + timedelta(minutes = query_iter * batch_size * binsizes[default_kline_size])
        data = bitmex_client.Trade.Trade_getBucketed(symbol=default_symbol, binSize=default_kline_size, count=batch_size,\
                                                 startTime = new_start_timestamp).result()[0]
        for i in range(len(data)):
            close_list.append(data[i]['close'])
            open_list.append(data[i]['open'])
            high_list.append(data[i]['high'])
            low_list.append(data[i]['low'])
            timestamp_list.append(data[i]['timestamp'])

    stored_vars={}
    stored_vars["timestamp_list"] = timestamp_list
    stored_vars["close_list"] = close_list
    stored_vars["open_list"] = open_list
    stored_vars["high_list"] = high_list
    stored_vars["low_list"] = low_list

    data_df = pd.DataFrame(list(zip(timestamp_list,low_list,high_list,open_list,close_list)), columns = ['time', 'low', 'high', 'open', 'close'])


    with open('data/bitmex_' + default_symbol + '_' + default_kline_size + '_' + start_timestamp.strftime(time_format) + '_' + end_timestamp.strftime(time_format) + '_list.pickle','wb') as handle:
        pickle.dump(stored_vars, handle, protocol = pickle.HIGHEST_PROTOCOL)
    data_df.to_pickle('data/bitmex_pandas_' + default_symbol + '_' + default_kline_size + '_' + start_timestamp.strftime(time_format) + '_' + end_timestamp.strftime(time_format) + '_list.pickle')
