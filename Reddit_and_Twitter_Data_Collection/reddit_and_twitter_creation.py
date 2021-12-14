#script for creating csv files from data using keywords_list

from datetime import datetime, timezone, timedelta, date
import pandas as pd
import pytz
#from twitter_data_collection import create_twitter_dataframe
from reddit_data_collection import create_reddit_dataframe



start_date_reddit = datetime(2020, 1, 1, 0)  #year, month, day, hour(0-23)
end_date_reddit = datetime(2020, 12, 31, 23)

utc=pytz.UTC
start_date_twitter = datetime(2020, 1, 1, 0,0,tzinfo=utc)  #year, month, day, hour(0-23), minute (0-59)
end_date_twitter = datetime(2020, 1, 2, 0,0,tzinfo=utc)  #inclusive

keywords_list = ["ethereum", "ETH"]
keywords_reddit = ""
keywords_twitter = ""

for keyword in keywords_list:
    if keywords_list.index(keyword) == 0:
        keywords_reddit = keywords_reddit + keyword

        keywords_twitter = keywords_twitter + keyword
    else:
        keywords_reddit = keywords_reddit + "|" + keyword
        keywords_twitter = keywords_twitter + " OR " + keyword


reddit_df = create_reddit_dataframe(keywords_reddit, start_date_reddit, end_date_reddit)
print(reddit_df)
reddit_df.to_csv('reddit_ethereum_ETH.csv')

#twitter_df = create_twitter_dataframe(keywords_twitter, start_date_twitter, end_date_twitter)
#print(twitter_df)
#twitter_df.to_csv('twit2.csv')