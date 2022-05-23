# group_04_project

This is the base project for Fall 2021 IE598/498 High Frequency Trading Group 04's project.

## Teammates
- Ghassan Shahatit - team leader - ghassan2@illinois.edu
- Michael Ruscito - ruscito2@illinois.edu
- Ranvir Rana - rbrana2@illinois.edu
- Daniel Bullock - djb6@illinois.edu

## Instructions for reading data

- Processed chain data is stored in `ethChainData/processed_data/filename.pickle`
  - It contains data from Ethereum (labelled as `eth` in filename) and Polygon (labelled as `polygon` in filename)
  - For each chain it contains transfer data for Chainlink (`LINK`), Maker (`MKR`) and Shiba Inu (`SHIB`)
  - Ethereum data is from November 30, 2021 to December 14, 2021. Polygon data is from December 12 to December 14, 2021
  - This range corresponds to 70K ethereum blocks and 200K polygon blocks respectively
  - Due to low time range, it is recommended to run classifier on a resolution of a minute
  - On the filename `1h` represents data aggregated every hour and `1m` represents data aggregated every minute.
  - There are 13 columns `["time", "meanVolume", "meanFromBalance", "meanToBalance", "medianVolume", "medianFromBalance", \
    "medianToBalance", "maxVolume", "maxFromBalance", "maxToBalance", "sumVolume", "sumFromBalance", "sumToBalance" ]` with time in `datetime.datetime`
  - Can be extracted using the command `pandas.read_pickle(filepath)`
- Price data from Coinbase can be fetched from their server itself since there is no discernable throttling.
  - Go to `priceData` folder
  - Run the command `python3(or pypy) coinbaseExplorer2.py symbol-name kline-size start-timestamp end-timestamp`
  - Symbol name tested are: `['BTC-USD', 'ETH-USD', 'DOGE-USD', 'SHIB-USD', 'LINK-USD', 'MKR-USD', 'ADA-USD']`
  - Use kline-size of `1h` or `1m`
  - Timestamp has the format: `"%Y-%m-%d %H:%M:%S"`
  - Here is an example command: `python3 coinbaseExplorer2.py BTC-USD 1m "2020-12-10 12:10:08" "2020-12-11 23:11:08"`
  - The data will be saved under the `data` folder with an example name `coinbase_BTC-USD_1m_2020-12-10 12:10:08_2020-12-11 23:11:08_list.pickle`
  - This data will be saved as a pandas dataframe, use `pandas.read_pickle(filename)`
  - There are 6 columns `["time", "low", "high", "open", "close", "volume"]`
