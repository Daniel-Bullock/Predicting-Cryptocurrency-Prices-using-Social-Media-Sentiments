import pickle
import time
from tqdm import tqdm
from datetime import timedelta, datetime
from dateutil import parser
import math
import sys
import pandas as pd
import json
import numpy as np

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: aggregator_pkl2pd.py blockchain symbol-name")
        sys.exit(1)

    blockchain = sys.argv[1]
    token = sys.argv[2]

    stored_vars = pickle.load(open('data/' + token + '_' + blockchain + '_transfer_list_final.pickle', 'rb'))

    timeStampList = stored_vars["timeStampList"]
    timeStampList1m = []
    timeStampList1h = []
    for i in range(len(timeStampList)):
        timeStampList1m.append(timeStampList[i][:17]+'00')
        timeStampList1h.append(timeStampList[i][:14]+'00:00')

    data1h = pd.DataFrame(list(zip(timeStampList1h,stored_vars["transferValueList"],stored_vars["transferFromBalanceList"],\
                                   stored_vars["transferToBalanceList"])), columns = ['time', 'volume', 'fromBalance', 'toBalance'])
    data1m = pd.DataFrame(list(zip(timeStampList1m,stored_vars["transferValueList"],stored_vars["transferFromBalanceList"],\
                               stored_vars["transferToBalanceList"])), columns = ['time', 'volume', 'fromBalance', 'toBalance'])

    data1h["time"] = pd.to_datetime(data1h["time"], infer_datetime_format=True)
    data1h["volume"] = pd.to_numeric(data1h["volume"])
    data1h["fromBalance"] = pd.to_numeric(data1h["fromBalance"])
    data1h["toBalance"] = pd.to_numeric(data1h["toBalance"])

    data1m["time"] = pd.to_datetime(data1m["time"], infer_datetime_format=True)
    data1m["volume"] = pd.to_numeric(data1m["volume"])
    data1m["fromBalance"] = pd.to_numeric(data1m["fromBalance"])
    data1m["toBalance"] = pd.to_numeric(data1m["toBalance"])

    column_list = ["time", "meanVolume", "meanFromBalance", "meanToBalance", "medianVolume", "medianFromBalance", \
                   "medianToBalance", "maxVolume", "maxFromBalance", "maxToBalance", "sumVolume", "sumFromBalance", "sumToBalance" ]

    stat_data1h = pd.merge(data1h.groupby(["time"]).mean(), data1h.groupby(["time"]).median(), on="time")
    stat_data1h = pd.merge(stat_data1h, data1h.groupby(["time"]).max(), on="time")
    stat_data1h = pd.merge(stat_data1h, data1h.groupby(["time"]).sum(), on="time")
    stat_data1h = pd.merge(pd.DataFrame(stat_data1h.index), stat_data1h, on="time")
    stat_data1h.columns = column_list

    stat_data1m = pd.merge(data1m.groupby(["time"]).mean(), data1m.groupby(["time"]).median(), on="time")
    stat_data1m = pd.merge(stat_data1m, data1m.groupby(["time"]).max(), on="time")
    stat_data1m = pd.merge(stat_data1m, data1m.groupby(["time"]).sum(), on="time")
    stat_data1m = pd.merge(pd.DataFrame(stat_data1m.index), stat_data1m, on="time")
    stat_data1m.columns = column_list

    stat_data1h.to_pickle('processed_data/' + token + '_' + blockchain + '_stat_pandas_1h.pickle')
    stat_data1m.to_pickle('processed_data/' + token + '_' + blockchain + '_stat_pandas_1m.pickle')