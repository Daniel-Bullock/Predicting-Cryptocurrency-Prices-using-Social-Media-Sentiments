import snscrape.modules.twitter as twitter
import pandas as pd
from datetime import datetime, timezone, timedelta, date
import pytz


#Example
#utc=pytz.UTC
#start_date = datetime(2021, 1, 1, 0,0,tzinfo=utc)  #year, month, day, hour(0-23), minute (0-59)
#end_date = datetime(2021, 1, 2, 0,0,tzinfo=utc)  #inclusive
#keywords = "bitcoin OR BTC"   #separate different keywords with " OR "
#twitter_dataframe = create_twitter_dataframe(keywords,start_date,end_date)
#print(twitter_dataframe)


def create_twitter_dataframe(keywords,start_date,end_date):
    #List to append tweet data to
    tweets_list = []

    #Declare variables
    utc=pytz.UTC  #used for timezone
    c=0   #count of tweets
    day_delta = timedelta(days=1)   #day time delta for the loop
    hour_delta = timedelta(hours=1)   #hour time delta for the loop
    current_date_and_hour = start_date  #keeps track of our current time

    while current_date_and_hour <= end_date:         #Looping over the days   
        if (current_date_and_hour + timedelta(hours=23)) < end_date:  #checks if it should loop over the full 24 hours for the day or stop earlier
            hour_end_date = current_date_and_hour + timedelta(hours=23) 
        else:  
            hour_end_date = end_date
        
        while current_date_and_hour <= hour_end_date:  #looping over the hours
            c= 0
        
            since = current_date_and_hour.strftime("%Y-%m-%d")   #converting time to string for input string
            since_plus_day = current_date_and_hour + day_delta  #used for twitter search, since and until has to have a day difference
            current_hour_plus_one = current_date_and_hour + hour_delta
            until = since_plus_day.strftime("%Y-%m-%d")
            search_input = keywords + " since:"  + since + " until:" + until

            #loops over every tweet from the since time to the until time containing the keywords
            for i,tweet in enumerate(twitter.TwitterSearchScraper(search_input).get_items()):
                if tweet.date < current_hour_plus_one and tweet.date > current_date_and_hour:  #if tweet is within hour currently at, add it to the count
                    c += 1   
            tweets_list.append([current_date_and_hour, c])   #apppend current time to the list with the count of tweets during that hour
            current_date_and_hour += hour_delta  #increment the hour
            

    #Convert to dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Count'])    

    return tweets_df


