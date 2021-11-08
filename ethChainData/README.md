# Ethereum Chain data extraction

This directory contains code that fetched token transfer data for ERC20 or derived tokens from the ethereum mainnet.

`chainWatcher1.ipynb` is a test code to check connection between web3 and infuria.

Run `python3 chainWatcher2.py https://mainnet.infura.io/v3/b40beb8540af492e968e6b67952443cc 1000` to extract
token transfer information regarding chainlink tokens and store them at `LINK-token-transfer.json`
I am pushing `LINK-token-transfer.json` file to gitlab for reference to my teammates. 

`jsonParser1` is a test code to extract useful time series from the token transfer data.

###PENDING:
- Write a parser to extract information compatible with the prediction model
- Extend code to other ERC20 derived tokens