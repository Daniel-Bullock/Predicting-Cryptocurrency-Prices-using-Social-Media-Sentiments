from csv import reader
import pandas as pd

def fetch_social_data(path):
    df = pd.read_csv(path)
    freq_list = df["Number of Posts"].to_list()
    return freq_list

#google_BTC = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_bitcoin.csv')
#print(google_BTC)
#google_ADA = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_cardano.csv')
#google_CHAIN = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_chainlink.csv')
#google_DOGE = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_dogecoin.csv')
#google_ETH = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_ethereum.csv')
#google_MKR = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_maker.csv')
#google_XRP = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/google_trends_ripple.csv')

#reddit_BTC = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_bitcoin.csv')
#reddit_ADA = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_cardano_ADA.csv')
#reddit_CHAIN = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_chainlink.csv')
#reddit_DOGE = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_dogecoin_DOGE.csv')
#reddit_ETH = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_ethereum_ETH.csv')
#reddit_MKR = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_maker.csv')
#reddit_XRP = fetch_social_data('Reddit_and_Google_Trends_Data_Collection/csv_files/reddit_ripple.csv')