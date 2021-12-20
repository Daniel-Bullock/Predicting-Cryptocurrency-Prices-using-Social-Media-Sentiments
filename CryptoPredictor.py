from NaiveBayes import NB
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
'''
def predict_price(coin_nb):

    nb = globals()[coin_nb] # lookup global variable for each coin's nb model

    # get price delta for past hour and add to NB training
    global last_social_data
    new_price_delta = 0#change
    last_hour_data = [last_social_data, new_price_delta]
    nb.train(last_hour_data)

    # optionally train other NB models
    nb.cnb_train(last_hour_data)
    nb.gnb_train(last_hour_data)

    # get current social data in list
    new_social_data = []#change
    last_social_data = new_social_data[0]

    # NB prediction
    prediction = nb.predict(new_social_data)

    # optionally predict with other NB models
    prediction2 = nb.cnb_predict(new_social_data)
    prediction3 = nb.gnb_predict(new_social_data)

    # do something with prediction

    return


if __name__ == "__main__":

    # global variables for later use
    last_social_data = 0
    
    # get historical social media data
    google_BTC = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_bitcoin.csv')
    google_ADA = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_cardano.csv')
    google_CHAIN = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_chainlink.csv')
    google_DOGE = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_dogecoin.csv')
    google_ETH = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_ethereum.csv')
    google_MKR = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_maker.csv')
    google_XRP = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_ripple.csv')

    reddit_BTC = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_bitcoin.csv')
    reddit_ADA = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_cardano_ADA.csv')
    reddit_CHAIN = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_chainlink.csv')
    reddit_DOGE = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_dogecoin_DOGE.csv')
    reddit_ETH = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_ethereum_ETH.csv')
    reddit_MKR = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_maker.csv')
    reddit_XRP = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_ripple.csv')

    # get historical coin pricing data
        # format price data into price deltas
    
    # combine historical data into list of tupes -> [(<social_data>, <price_delta>), ...]
        # can use zip(list1, list2), then for item in zip -> append to empty list
    btc_data = []#change
    eth_data = []#change
    
    # create Naive Bayes predictors for each coin
        # passing data during instantiation trains models with data
    btc_nb = NB(btc_data)
    eth_nb = NB(eth_data)

    # optionally train other NB models
    btc_nb.cnb_train(btc_data)
    btc_nb.gnb_train(btc_data)
    eth_nb.cnb_train(eth_data)
    eth_nb.gnb_train(eth_data)

    # I do not know how well this scheduler will work, but something to try
    #    supposed to call predict_price every hour
    # call predict on new data every hour
    scheduler = BlockingScheduler()
    scheduler.add_job(predict_price, 'interval', args=["btc_nb"], hours=1)  # BTC prediction
    scheduler.add_job(predict_price, 'interval', args=["eth_nb"], hours=1)  # ETH prediction
    scheduler.start()
'''

# Simplest way to run:
# requires complete re-training every time
train_no = 8500 #7784
# get complete social data
df = pd.read_csv('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_bitcoin.csv')
google_BTC = df["Number of Posts"].to_list()
google_BTC_dates = df["date"].to_list()
df = pd.read_csv('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_ethereum.csv')
google_ETH = df["Number of Posts"].to_list()
google_ETH_dates = df["date"].to_list()
df = pd.read_csv('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_bitcoin.csv')
reddit_BTC = df["Number of Posts"].to_list()
reddit_BTC_dates = df["date"].to_list()
df = pd.read_csv('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_ethereum_ETH.csv')
reddit_ETH = df["Number of Posts"].to_list()
reddit_ETH_dates = df["date"].to_list()

# remove duplicate dates in google data
index = []
offset = 0
for i in range(len(google_BTC_dates)-1):
    if google_BTC_dates[i] == google_BTC_dates[i+1]:
        index.append(i)
for i in index:
    del google_BTC[i-offset]
    offset += 1

index = []
offset = 0
for i in range(len(google_ETH_dates)-1):
    if google_ETH_dates[i] == google_ETH_dates[i+1]:
        index.append(i)
for i in index:
    del google_ETH[i-offset]
    offset += 1

# get complete price data
df_btc = pd.read_csv('priceData/gitlabData/coinbase_pandas_BTC-USD_1h_2020-01-01 00_00_00_2020-12-31 23_00_00_list.csv')
btc_usd_open = df_btc["open"].to_list()
btc_usd_close = df_btc["close"].to_list()

df_eth = pd.read_csv('priceData/gitlabData/coinbase_pandas_ETH-USD_1h_2020-01-01 00_00_00_2020-12-31 23_00_00_list.csv')
eth_usd_open = df_eth["open"].to_list()
eth_usd_close = df_eth["close"].to_list()

# convert to deltas
btc_results = []
btc_prices = []
for open, close in zip(btc_usd_open, btc_usd_close):
    delta = close - open
    btc_prices.append(delta)
    if delta > 0:
        btc_results.append(1)
    elif delta == 0:
        btc_results.append(0)
    else:
        btc_results.append(-1)

eth_results = []
eth_prices = []
for open, close in zip(eth_usd_open, eth_usd_close):
    delta = close - open
    eth_prices.append(delta)
    if delta > 0:
        eth_results.append(1)
    elif delta == 0:
        eth_results.append(0)
    else:
        eth_results.append(-1)

btc_results = btc_results[train_no:]
eth_results = eth_results[train_no:]

# separate into train & test data
btc_train_google = google_BTC[0:train_no]   # total 8784 lines
btc_test_google = google_BTC[train_no:]
btc_train_reddit = reddit_BTC[0:train_no]
btc_test_reddit = reddit_BTC[train_no:]

eth_train_google = google_ETH[0:train_no]
eth_test_google = google_ETH[train_no:]
eth_train_reddit = reddit_ETH[0:train_no]
eth_test_reddit = reddit_ETH[train_no:]

btc_prices = btc_prices[0:train_no]
eth_prices = eth_prices[0:train_no]

# zip together with price data
zip_btc_train_google = zip(btc_train_google, btc_prices)
zip_btc_train_reddit = zip(btc_train_reddit, btc_prices)
zip_eth_train_google = zip(eth_train_google, eth_prices)
zip_eth_train_reddit = zip(eth_train_reddit, eth_prices)

btc_train_google = []
btc_train_reddit = []
eth_train_google = []
eth_train_reddit = []
for data in zip_btc_train_google:
    btc_train_google.append(data)
for data in zip_btc_train_reddit:
    btc_train_reddit.append(data)
for data in zip_eth_train_google:
    eth_train_google.append(data)
for data in zip_eth_train_reddit:
    eth_train_reddit.append(data)

# make NB models for each coin/social
btc_nb_google = NB()
btc_nb_reddit = NB()
eth_nb_google = NB()
eth_nb_reddit = NB()

# run predictions
btc_google1, btc_google2, btc_google3 = btc_nb_google.full_suite(btc_train_google, btc_test_google, log=False)
btc_reddit1, btc_reddit2, btc_reddit3 = btc_nb_reddit.full_suite(btc_train_reddit, btc_test_reddit, log=False)
eth_google1, eth_google2, eth_google3 = eth_nb_google.full_suite(eth_train_google, eth_test_google, log=False)
eth_reddit1, eth_reddit2, eth_reddit3 = eth_nb_reddit.full_suite(eth_train_reddit, eth_test_reddit, log=False)

# do something with predictions
# calculate percentage correct
btc_google1_correct = 0
btc_google2_correct = 0
btc_google3_correct = 0
for i in range(len(btc_google1)-1):
    if btc_google1[i] == btc_results[i]:
        btc_google1_correct += 1
    if btc_google2[i] == btc_results[i]:
        btc_google2_correct += 1
    if btc_google3[i] == btc_results[i]:
        btc_google3_correct += 1
    
btc_reddit1_correct = 0
btc_reddit2_correct = 0
btc_reddit3_correct = 0
for i in range(len(btc_reddit1)-1):
    if btc_reddit1[i] == btc_results[i]:
        btc_reddit1_correct += 1
    if btc_reddit2[i] == btc_results[i]:
        btc_reddit2_correct += 1
    if btc_reddit3[i] == btc_results[i]:
        btc_reddit3_correct += 1

eth_google1_correct = 0
eth_google2_correct = 0
eth_google3_correct = 0
for i in range(len(eth_google1)-1):
    if eth_google1[i] == eth_results[i]:
        eth_google1_correct += 1
    if eth_google2[i] == eth_results[i]:
        eth_google2_correct += 1
    if eth_google3[i] == eth_results[i]:
        eth_google3_correct += 1
    
eth_reddit1_correct = 0
eth_reddit2_correct = 0
eth_reddit3_correct = 0
for i in range(len(eth_reddit1)-1):
    if eth_reddit1[i] == eth_results[i]:
        eth_reddit1_correct += 1
    if eth_reddit2[i] == eth_results[i]:
        eth_reddit2_correct += 1
    if eth_reddit3[i] == eth_results[i]:
        eth_reddit3_correct += 1

btc_google1_percent = btc_google1_correct/len(btc_google1)
btc_google2_percent = btc_google2_correct/len(btc_google2)
btc_google3_percent = btc_google3_correct/len(btc_google3)
btc_reddit1_percent = btc_reddit1_correct/len(btc_reddit1)
btc_reddit2_percent = btc_reddit2_correct/len(btc_reddit2)
btc_reddit3_percent = btc_reddit3_correct/len(btc_reddit3)

eth_google1_percent = eth_google1_correct/len(eth_google1)
eth_google2_percent = eth_google2_correct/len(eth_google2)
eth_google3_percent = eth_google3_correct/len(eth_google3)
eth_reddit1_percent = eth_reddit1_correct/len(eth_reddit1)
eth_reddit2_percent = eth_reddit2_correct/len(eth_reddit2)
eth_reddit3_percent = eth_reddit3_correct/len(eth_reddit3)

print("BTC Google %: ", str(btc_google1_percent), str(btc_google2_percent), str(btc_google3_percent))
print("BTC Reddit %: ", str(btc_reddit1_percent), str(btc_reddit2_percent), str(btc_reddit3_percent))
print("ETH Google %: ", str(eth_google1_percent), str(eth_google2_percent), str(eth_google3_percent))
print("ETH Reddit %: ", str(eth_reddit1_percent), str(eth_reddit2_percent), str(eth_reddit3_percent))
