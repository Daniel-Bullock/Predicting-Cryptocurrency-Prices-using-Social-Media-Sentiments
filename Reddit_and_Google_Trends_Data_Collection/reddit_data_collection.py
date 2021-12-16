import psaw
from datetime import datetime, timezone, timedelta, date
from psaw import PushshiftAPI
import pandas as pd


#example
#start_date = datetime(2020, 1, 1, 12)  #year, month, day, hour(0-23)
#end_date = datetime(2020, 1, 1, 23)
#keywords ='Ripple|XRP' #separate keywords with OR(|) operator (no space)
#reddit_df = create_reddit_dataframe(keywords, start_date, end_date)  #creates dataframe for these keywords
#print(reddit_df)


def create_reddit_dataframe(keywords, start_date, end_date):
    api = PushshiftAPI()    #declare api
    delta = timedelta(hours=1)   #time delta for the loop
    inter_date = start_date + delta #intermediate date an hour ahead

    #initialize dataframe
    subs = api.search_submissions(after=int(start_date.timestamp()),before=int(inter_date.timestamp()),subreddit="CryptoCurrency",q= keywords,max_results_per_request=100)
    initialize_frequency = 0
    for post in subs:
            initialize_frequency += 1
    df = pd.DataFrame({'Date':[start_date],'Number of Posts':[initialize_frequency]})
    start_date += delta  
    inter_date += delta  
    
    while start_date <= end_date:  #loops from start_date to end_date by 1 hour increments
        #create subreddit generator
        subs = api.search_submissions(       
            after=int(start_date.timestamp()),
            before=int(inter_date.timestamp()),
            subreddit="CryptoCurrency",
            q= keywords,
            #max_results_per_request=100       #add this in case this is throwing a lot of backoff errors
            )    

        #count every post in generator instance
        c = 0 
        for post in subs:  
            c += 1

        #add row with the current hour and number of posts that hour
        df_append = {'Date':start_date,'Number of Posts':c} 
        df = df.append(df_append, ignore_index=True)
    
        start_date += delta   #incrementors for loop
        inter_date += delta

    return df



