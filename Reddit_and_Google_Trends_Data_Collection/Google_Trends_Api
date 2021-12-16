from pytrends.request import TrendReq
import pandas as pd 

pytrends = TrendReq(hl='en-US', tz=360) 

keywords1 = ["bitcoin", "BTC", "XBT", "GBTC", "BITO"]
keywords2 =["Ethereum", "ETH"]
keywords3 =  ["DogeCoin", "DOGE"]
keywords4= ["Maker", "MKR"] 
keywords5 = ["Chainlink", "CHAIN"]
keywords6= ["Cardano", "ADA"] 
keywords7 = ["Ripple", "XRP"] 

pytrends.build_payload(keywords1, cat=0, timeframe='today 5-y') 

google_df1=pytrends.get_historical_interest(keywords1, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=12, day_end=31, hour_end=23, cat=0, sleep=0)
google_df2=pytrends.get_historical_interest(keywords2, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=12, day_end=31, hour_end=23, cat=0, sleep=0)
google_df3=pytrends.get_historical_interest(keywords3, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=12, day_end=31, hour_end=23, cat=0, sleep=0)
google_df4=pytrends.get_historical_interest(keywords4, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=12, day_end=31, hour_end=23, cat=0, sleep=0)
google_df5=pytrends.get_historical_interest(keywords5, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=12, day_end=31, hour_end=23, cat=0, sleep=0)
google_df6=pytrends.get_historical_interest(keywords6, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=12, day_end=31, hour_end=23, cat=0, sleep=0)
google_df7=pytrends.get_historical_interest(keywords7, year_start=2020, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=12, day_end=31, hour_end=23, cat=0, sleep=0)


google_df1['frequency_bitcoin'] = google_df1['bitcoin'] + google_df1['BTC'] + google_df1['XBT'] + google_df1["GBTC"] + google_df1["BITO"]
google_df2['frequency_ethereum'] = google_df2['Ethereum'] + google_df2['ETH']
google_df3['frequency_dogecoin'] = google_df3['DogeCoin'] + google_df3['DOGE']
google_df4['frequency_maker'] = google_df4['Maker'] + google_df4['MKR']
google_df5['frequency_chainlink'] = google_df5['Chainlink'] + google_df5['CHAIN']
google_df6['frequency_cardano'] = google_df6['Cardano'] + google_df6['ADA']
google_df7['frequency_ripple'] = google_df7['Ripple'] + google_df7['XRP']

#google_df = google_df1.copy()
#google_df["frequency_ethereum"] = google_df2["frequency_ethereum"]
#google_df["frequency_dogecoin"] = google_df2["frequency_dogecoin"]
#google_df["frequency_ripple"] = google_df3["frequency_ripple"]
#google_df["frequency_maker"] = google_df3["frequency_maker"]
#google_df["frequency_chainlink"] = google_df4["frequency_chainlink"]
#google_df["frequency_cardano"] = google_df4["frequency_cardano"]

#print(google_df)

google_df1.to_csv('google_trends_bitcoin.csv')
google_df2.to_csv('google_trends_ethereum.csv')
google_df3.to_csv('google_trends_dogecoin.csv')
google_df4.to_csv('google_trends_maker.csv')
google_df5.to_csv('google_trends_chainlink.csv')
google_df6.to_csv('google_trends_cardano.csv')
google_df7.to_csv('google_trends_ripple.csv')

