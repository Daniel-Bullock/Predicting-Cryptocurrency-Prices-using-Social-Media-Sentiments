# Group 04 Project Report: Predicting Cryptocurrency Price Fluctuations Using Social, Websearch and Blockchain Media

## Introduction

A model for predicting price movements of cryptocurrencies based on publicity trends on social media and on-chain transaction data. Training data fed into predictive models consists of previous trends and associated cryptocurrency price changes for various coins, and live data of publicity trends for coins serves as test data for models to predict price movements. 2 predictive models - naive bayes for classification and long short-term memory model as a model for granular predictions. We put the proverb “All publicity is good publicity” to test! 


## Social media data collection

We retrieved Reddit data from the subreddit CryptoCurrency using the PushShift API Wrapper package. We only tested one subreddit because of how long the computation time took to retrieve this data due to inadequacies with the Reddit API. We chose the CryptoCurrency subreddit because we think it has a good balance of people posting very reasonable and genuine questions, relevant news articles, and people just stating their opinions. Other cryptocurrency related subreddits had a lot of posts which would just be focused on humor. We used the frequency of posts on the subreddit in an hour span from January 1st to December 20th of 2020 to train the data for the Naive Bayes and the rest of the year to run it on. A potential source of error for this data could be that we checked for search terms involving each coin in the title, sometimes the title might not actually be about said coin. Also no sentiment analysis was done on each post, so whenever it was a negative article it would only affect the prediction in the positive direction. 

We retrieved Google Trends data from the PyTrends package. We used the historical hourly interest from our search terms which is historical, indexed, hourly data for when the keyword was searched most as shown on Google Trends' Interest Over Time section. Each hour is a ratio from the current hour’s number of searches to the highest number of searches over the entire time period searched (one year). This was the only way of retrieving any sort of relevant data which could be a major form of error because we combined multiple search terms’ hourly interest together, which would make the final hourly interest ratio we gathered a ratio of multiple highpoints added up.


## Chain data collection

Transactions of all ERC20 tokens (ERC20 is a token standard on ethereum) are recorded on the ethereum blockchain. 
LINK, SHIB ank MKR are popular ERC20 tokens, hence we collect data on the blockchain for price inference. 
We have implemented a two stage setup to collect transaction and account data from the ethereum blockchain. 
We connect to a full node through the web3 API, our full node provider is a free account on Infuria. 
The two stages are listed as below:

- *Chainwatcher*: This program fetches all transaction data stored in the past x blocks on the ethereum network. 
The main web3 call instantiated by this module is `GetBlocks(Block number)`. This request fetches the block at the height of BlockNumber
on the blockchain. The block consists of all transactions and their corresponding receipts. A receipt in ethereum
corresponds to the details of state changes incurred by the said transactions. From these transactions we filter out transactions
that correspond to the ERC20 token of our choice. Each ERC20 token transfer passes through its contract, hence we filter
out transactions that call the `transfer` method of the corresponding contract. We store the details of the transactions in a json.
This code is implemented at `ethChainData/token-transfer-state.json`
- *StateExtractor*: The state extractor takes the above json file and scans through all transaction participants, it fetches
the balances of all transaction participants by using web3.py API `balanceOf(Account)` request. Thus, we have the following information for each individual transaction:
  - Transaction value
  - Balance of sending party
  - Balance of receiving party

The data is then parsed and stored in a pandas dataframe with data aggregated into time slots. The time slots we use are
`1m` and `1h`. Transaction data is aggregated within a time slot into these 4 signals:
- Mean
- Median
- Max
- Sum

Thus generating a total of 12 data points per time slot.

<img src="images/chainWatcher.png" alt="ChainWatcher" width="500"/>

Note that with the advent of side chains like polygon, many transfer of tokens occur on these sidechains, the same 
code with certain modifications (changing contract address for example) can be used to fetch polygon chain data. 
Our current codebase supports that. The code for ChainWatcher can be found under: `ethChainData/chainWatcher2.py` 
and that for StateExtractor + parser can be found at `ethChainData/jsonParserOptimized.py`. Instructions to run this 
code can be found under `ethChainData/README.md`. We collect data of past 70k ethereum blocks (Nov 30, 2021 to Dec 12, 2021).

## Price data collection

We use Bitmex and Coinbase API to gather price data on the tokens. We use these two exchanges since historical XRP data 
is available on Bitmex and not on Coinbase and historical SHIB data is available on Coinbase and not on Bitmex.

We use the `requests` library to make requests to Coinbase’s API endpoint: `api.pro.coinbase.com`. The requests are made
for a trading pair (Token-USD) within a given time frame, each data point being candle price data for a given time granularity (`1m` or `1h`).
The requests are made as `”https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}”`. The response is parsed
and stored as a pandas dataframe consisting of the following columns: `[timeslot, open, close, high, low, volume]`.

We use Bitmex's python library to make calls to their API endpoint. The library’s `Trade.Trade_getBucketed` method requests the 
bucketed prices of a particular trading pair (Token-USD) within a given time range within a given time granularity (`1m` or `1h`) 
and automatically parses the received response. Each entry in the response consists of `[timeslot, open, close, high, low]`. 
This response is then stored in a pandas dataframe. The code for this implementation can be found at: `priceData/bitmexExplorer2.py`.

For the Naive Bayes classification we fetch price data with a `1h` granularity between Jan 1, 2020 to Dec 31, 2020. 
For LSTM price prediction we fetch price data at a granularity of `1m` from Nov 30, 2021 to Dec 12, 2021. Instructions on how to run 
these programs are provided at `priceData/README.md`.

## Naive Bayes Classifier

We implemented 3 Naive Bayes models: NB classifier (modified multinomial NB), and 2 NB models from the scikit-learn library - CategoricalNB and Gaussian NB. The NB classifier uses laplace smoothing and takes the log of calculated probabilities to prevent underflow. The results from the NB models were less than promising. The results of the NB testing after 8500 data points can be seen in the figure below. Despite the GaussianNB appearing to have the best accuracy, it always predicted a price increase except for the ETH Reddit data. The NB classifier and CategoricalNB made identical predictions, yet were overly bearish as they performed worse than the prediction of always increasing price.

<img alt="NB_Results" src="images/NB_Results.png" width="500"/>

Naive Bayes are methods of well-defined learning algorithms based on Bayes' theorem and the assumption of conditional dependence between the training variables. The derivation of the basic Naive Bayes relationship is shown below. Each of the NB models differ by making various assumptions about the distribution of the relationship between the conditionally dependent variables.

<img alt="NB_Math" src="images/NB_Math.png" width="500"/>

The NB Classifier uses the following equation in its predictive model:

<img alt="ClassifierNB_equation" src="images/ClassifierNB_equation.png" width="500"/>

The CategoricalNB uses a similar equation:

<img alt="CategoricalNB_equation" src="images/CategoricalNB_equation.png" width="500"/>

And the GaussianNB makes the assumption of a gaussian distribution between the conditionally dependent variables shown below:

<img alt="GaussianNB_equation" src="images/GaussianNB_equation.png" width="500"/>

The inputs for the training stage of each of our NB models included the social media data for a coin from a single source (i.e. Google Trends OR Reddit, each media has its own separate training), and the coin's price delta for the past hour. These values are zipped together and fed into the training functions as a list of tuples formatted [ (float< social data >, float< price change >), ... ]. The input to the prediction functions is only the social media data for the coin over the past hour, and this outputs the NB prediction of the coin's price's direction. The NB functions as a classifier, so the output classifies the price direction into whether the price will increase, decrease, or remain stagnant. The coin's prices in both the input and the prediction are not weighted. Additionally, the range for a price to be "stagnant" is only +/-$0.01, so this is a rare occurance and as a result none of the predictive models ever output a stagnant price because the prior probability is too low. For a more risk averse model, this range should be increased. Our suggestion is to increase the range of a "stagnant" price to a set small percentage of the coin's price. This way the model only treats a more significant price delta as an increase or decrease in price and will always cover the transaction costs of buying/selling the coin.

The results of the GaussianNB indicate that there is certainly not a gaussian distribution in the relationship between the social media data and price deltas of Bitcoin, and potentially only a weak gaussian distribution between reddit data and Ethereum prices since the GaussianNB always predicted a price increase except in the case of the ETH Reddit model. The relationship between Bitcoin and Google Trends/Reddit mentions are shown in the scatter plots below. The x-axis for each graph is the social media data (discussed in the section above), and the y-value is the discrete price delta classes (1.0=increase, 0.0=stagnant, -1.0=decrease). The size of the dot on the scatter plot indicates the frequency of that input (i.e. Reddit data with 0 mentions is very common and so there is a noticably large amount of inputs with 0 reddit mentions and both price increases and decreases). As seen in the graphs, there is hardly any distinguishable relationship between price decreases and increases for BTC based on the Google trend data since the upper and lower sections of the graph appear to mirror each other very closely. Similaryly, the Reddit data is seemingly mirrored, but has some distinction and can be seen in the more accurate prediction results from the NB models. Also notable is that there are very few occurances of stagnant prices.

<img alt="BTC_Google_Correlation" src="images/BTC_Google_Correlation.png" width="500"/>
<img alt="BTC_Reddit_Correlation" src="images/BTC_Reddit_Correlation.png" width="500"/>

Below are the tables showing the percentages of true and false positives and negatives for both BTC and ETH based on both Google Trend and Reddit data. The tables indicate the percentage of the time the actual price delta was increased how often the models predicted a price increase, etc. The BTC predictions based on Google Trend data was very poor and actually had a negative effect indicted by the percentage to the right of the graph. The rest of the models all had positive results.

<img alt="BTC_TF_PN" src="images/BTC_TF_PN.png" width="500"/>
<img alt="ETH_TF_PN" src="images/ETH_TF_PN.png" width="500"/>

Some of the conclusions we can draw from the Naive Bayes models is that Reddit data is a better indicator of price direction than Google Trends. However, both of these models were still worse than simply always predicting a price increase which is discouraging. This is due to the overly bearish predictions from the models. Additionally, the price of Ethereum follows the social data more closely than Bitcoin as seen by the true/false positives/negatives impacts. We hypothesize that this effect would be even more amplified for less popular coins that are more likely to have higher volatility driven by retail traders.

A few possible contributions to the error in our NB models could be the following:
- Format of Google Trends data - represents interest relative to highest point in given range
- Lack of popularity in Reddit data - high amount of 0 or 1 mentions
- Lack of training data - Only trained from Jan. 1, 2020 to Dec. 20, 2020
  - Testing with more training indicated better prediction accuracies
  - Not trained on an entire calendar year
- Lack of stagnant price range
  - Current implementation has +/- $0.01 range for stagnant price

In addition to the NB models that were implemented, we additionally implemented some tools that went unutilized. We created a scheduler that trains the NB models on historical data once, then tests hourly on real-time social media data. With the scheduler also includes continuous training which stores the previous hour's social data in a buffer during continuous testing and then pairs it with the most recent price delta and adds them to the training model. The reason these tools went unutilized was that they were limited by the API calls needing to function every hour which was not available.

## LSTM predictor

We use neural networks to predict the price of ERC20 tokens using past price data and chain data as input. LSTM (Long Short-Term Memory)
networks are a class of Recurrent neural networks, the de-facto NNs used for analyzing time series data. LSTMs can generalize 
to utilize more historical context of the data by storing and forwarding a context state to future invocations. The code for training 
the LSTM can be found at `LSTM_model/LSTMpredictor.py` and the code for plotting results of the trained networks can be found at `LSTM_model/LSTM_explorer.ipynb`.

We deploy a LSTM with 3 layers, each hidden layer has a dimension of 64. As in input to the LSTM, we provide the past 50 data points. 
The latest past data is (leeway+1) time steps before the current timestep, we set leeway = 10, hence we are predicting prices 11 minutes in advance.
Each past data point consists of 16 dimensions:
- Past open, past close, past high, past low [4]
- Mean, median, max and sum of the transaction transfer values and balances of parties sending and receiving tokens [4*3=12]

We set the optimizer loss as MSE loss and use Adam optimizer at a learning rate of 0.01. The class defining the LSTM network can be 
found under `LSTM_predictor.py` as `LSTM` and the method for loading data is defined as `load_data` under the same file. 
The price and chain data is gathered at a granularity of `1m` for the time ranging from Nov 30, 2021 to Dec 12, 2022. 
67% of the data is used for training and 33% is used for testing. The results of running the predictor on testing data for LINK, SHIB and MKR token are plotted below:

<img alt="Chainlink1" src="images/LINK1.png" width="500"/>

RMSE error for LINK is 0.15. Although the above plot looks very accurate, we can find the flaws in the prediction when 
we zoom into a small time range.

<img alt="Chainlink2" src="images/LINK2.png" width="500"/>

We observe that the plot of predicted price lags the plot of actual price by approximately 10 minutes: the same number as 
the leeway. This implies that the LSTM predictor is giving a lot of weight to the price data in the immediate past and a 
lot less weight to the chain data. We can improve on this by (a) Modifying LSTM architecture, (b) Modifying loss function 
and (c) using training hacks like input randomization. We leave these approaches for future work. Please find the prediction 
results for MKR and SHIB below.

<img alt="ShibaInu1" src="images/SHIB1.png" width="500"/>

<img alt="Maker1" src="images/MKR1.png" width="500"/>

## Contributions

Ranvir
- Wrote code to fetch and parse Ethereum and Polygon chain data; this code can be found in the `ethChainData` folder
- Wrote code to fetch and parse price data from Coinbase and Bitmex; this code can be found in the `priceData` folder.
- Wrote code to train and test LSTM predictor, this code can be found in the `LSTM_model` folder
- Wrote code to plot results of the LSTM predictor

Ghassan
- Contributed to Google Trends API
- In charge of twitter (tweepy) API that didn’t work out (due to pricing and data limitations)
- Contributed to Reddit API
- Team Leader

Daniel
- Contributed to Google Trends API
- Wrote script for data cleaning
- Contributed to Reddit API
- Researched different twitter APIs to try to find a functional one

Michael
- Wrote library for Naive Bayes training and testing functions, including the NB clasifier, CategoricalNB, and Gaussian NB; this code can be found in the `NaiveBayes.py` file
- Wrote scirpt for data cleaning (removing duplicate entries to google trend data, and fixing missing entries of price data)
- Wrote code to conjoin social data with price data and train & test each NB model for BTC and ETH based on google trend and reddit data; this code can be found in the `CryptoPredictor.py` file
- Ran analysis of NB results including plotting social data & price correlation, and calculating accuracies of each model with true/false positives/negatives
- Wrote code to launch a scheduler for real-time NB testing with continuous training; this code can be found in the commented out section of the `CryptoPredictor.py` file
- Performed initial project research and based project idea on [this paper](https://www.researchgate.net/publication/279917417_Bitcoin_Spread_Prediction_Using_Social_And_Web_Search_Media)
