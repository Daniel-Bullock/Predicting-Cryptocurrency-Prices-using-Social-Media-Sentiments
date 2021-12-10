# Bitmex exchange data extractor

`bitmexExplorer1.ipynb` is a testing file. `bitmexExplorer2.py` is the relavant file.

Should be called as : `bitmexExplorer2.py symbol-name kline-size start-timestamp end-timestamp` as an example
call`python3 bitmexExplorer2.py LINKUSD 1h None None`. 

The timeseries lists will be stored at `data/bitmex_symbol_klineSize_list.pickle`