# Chain data extraction for Ethereum like chains, example - Ethereum mainnet and Polygon mainnet

This directory contains code that fetched token transfer data for any ERC20 or derived tokens from the ethereum mainnet.

`chainWatcher1.ipynb` is a test code to check connection between web3 and infuria.

Run `python3 chainWatcher2.py eth 1000 LINK 0x514910771af9ca656af840dff83e8264ecf986ca
` to extract
token transfer information regarding chainlink tokens from the ethereum mainnet and store them at `data/LINK-token-transfer.json`
I am pushing `LINK-token-transfer.json` file to gitlab for reference to my teammates. 

`jsonParser1` is the code to extract useful time series from the token transfer data.

`chainwatcher2.py` is now generalized to support both ethereum mainnet and polygon mainnet.

Some example calls are:
- `python3 chainWatcher2.py polygon 1000 LINK 0x53e0bca35ec356bd5dddfebbd1fc0fd03fabad39`
