# Project Description
A model for predicting price movements of cryptocurrencies based on publicity trends on social media and on-chain transaction data. Training data fed into predictive models consists of previous trends and associated cryptocurrency price changes for various coins, and live data of publicity trends for coins serves as test data for models to predict price movements. 3 predictive models - naive bayes for classification, hidden markov model for more granularity (predict actual price movement amounts), and long short-term memory model as separate model for granular predictions. We put the proverb “All publicity is good publicity” to test! 

## Research and Development Needed
* Literature review
* Prediction model that combines both off-chain social media data and on-chain data

For research, we will look into literature related to our project, looking into projects similar to ours to see how they analyzed the data. We will look into a time-series prediction model that combines both off-chain social media data and on-chain data.  As of right now, we think we will set up an HMM and LSTM, but we might change that if we find a better model to use.

## Data Sources/API
* Google trends  - Pytrends
* Twitter - Tweepy 
* Reddit/r/CryptoCurrency - PRAW
* Ethereum chain-data (ERC-20 token only)
  * Use Web3.py-API connected to a data provider like Infuria or an personal ethereum full node or
  * Use etherscan API 
* Exchange data - CoinGecko REST API
* BTC, ETH, DOGE, SHIB, XRP, and ADA
* As well XBT, GBTC, and BITO (symbols and tickers that trade alongside bitcoin price movement)

We will analyze the trends of Bitcoin(BTC), XBT, GBTC, BITO, Ethereum, DogeCoin, Shiba Inu Coin, Ripple, Maker (MKR), Chainlink(LINK) and Cardano. We are interested in these coins primarily because they have such large and enthusiastic communities online. Hence, there is often much constant discussion of these coins, especially amongst retail traders. We will use Pytrends as our API for Google trends, Tweepy as our API for Twitter, and PRAW as our API for Reddit, more specifically the /r/CryptoCurrency subreddit. We will extract data of the amount of times the tag/full name was searched/used on the platforms per hour/day.  Some of the tokens listed above are ERC20 tokens (or have their wrapped counterparts on Ethereum); thus, gathering the state of their ERC20 contracts through on-chain data can help make price predictions. We plan on using Web3 APIs connected to a blockchain data provider: a personal full node or Infuria; alternatively, we can use Etherscan’s API to gather more processed data. For exchange data to gather pricing information, we will use the CoinGecko REST API.

## Prediction Models
We will implement 3 layers of predictive models for different granularity in predictions and different models for hopefully improved accuracy. The inputs to each function is training data and test data. The training data is a history of publicity trends from a single source (Google trends or twitter, etc) and the associated price change at the same time as the trend data. The test data is the current trend data for the cryptocurrency.

The first model we will use is a naive bayes classifier to predict if the crypto price will move up, down, or remain stagnant. The Naive bayes uses bayes theorem for predicting P(price up | search trend) = P(search trend | price up) * P(price up) / P(search trend). The price changes are unweighted for a trend. The output from our naive bayes model will be a single value indicating the predicted direction of the cryptocurrency’s price.

The second model we will use is a hidden markov model to predict the exact value that the price will change by. This model will average the changes of a coin for given trend data, average neighboring trend data for unseen values, and use the averages as a prediction for the price change. This is a similar predictive model to the naive bayes but the price changes are weighted for trend data and are given more context to surrounding data. The output of our HMM model is a signed floating point value indicating the predicted price delta and direction for the cryptocurrency.

To generalize the effects of context in our time-series prediction problem, we use a class of Recurrent Neural networks - Long Short-Term Memory (LSTM) neural networks. The past input data time series and output price time series will be used to train our LSTM network to learn the dependencies of price on the current input data and a dynamically weighted set of past input data.

Several layers/models:
* First using Naive Bayes classifier for predicting if crypto price will move up/down/stagnant
  * Bayes theorem for predicting P(price up | search trend) = P(search trend | price up) * P(price up) / P(search trend)
* More complex model of above for guessing actual price movement (HMM)
* LSTM based price predictor

## Steps/Timeline
* Data time-series creation by 11/04
* Naive Bayes Classifier by 11/11
* Classifier testing by 11/18
* HMM / LSTM based price predictor by 11/25
* Price estimator testing - Hyperparameter adjustment by 12/2
* Finalize by 12/9
* (As of now, this timeline will most likely change as we progress, find issues and change ideas)
* (We will meet once a week and we will properly add our work to the git repository)

## Deliverables
* Trend Classifier 
* Price estimator
* Performance metrics - Accuracy, Precision for classifier, LogLoss for price estimator

## Tentative Task Allocation
* Michael - Naive Bayes & HMM functions
* Ranvir - Ethereum chain data APIs, Exchange data API, LSTM based predictor
* Daniel - Twitter, Reddit APIs 
* Gus - Google Trends APIs, Processing data into format the data expects, group manager (flex role)

### Future of Project (not anticipating implementing):
* Weighting analysis of various trend sources into a single prediction
* Sentiment analysis
