from NaiveBayes import NB
from apscheduler.schedulers.blocking import BlockingScheduler


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

    ''' I do not know how well this scheduler will work, but something to try
        supposed to call predict_price every hour'''
    # call predict on new data every hour
    scheduler = BlockingScheduler()
    scheduler.add_job(predict_price, 'interval', args=["btc_nb"], hours=1)  # BTC prediction
    scheduler.add_job(predict_price, 'interval', args=["eth_nb"], hours=1)  # ETH prediction
    scheduler.start()

'''
# Simplest way to run:
# requires complete re-training every time
# get complete social data
# get complete price delta data
btc_nb = NB()
# get current social data
prediction1, prediction2, prediction3 = btc_nb.full_suite(btc_data, new_social_data)
# do something with predictions
'''
