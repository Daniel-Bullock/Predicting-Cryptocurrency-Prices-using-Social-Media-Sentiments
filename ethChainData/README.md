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
- `python3 chainWatcher2.py polygon 200000 LINK 0x53e0bca35ec356bd5dddfebbd1fc0fd03fabad39`
- `python3 chainWatcher2.py eth 70000 SHIB 0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce`
- `python3 chainWatcher2.py eth 70000 MKR 0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2`
- `python3 chainWatcher2.py polygon 200000 MKR 0x6f7C932e7684666C9fd1d44527765433e01fF61d`
- `python3 chainWatcher2.py polygon 200000 SHIB 0x6f8a06447ff6fcf75d803135a7de15ce88c1d4ec`

Some example calls for jsonParserOptimized.py are:
- `python3 jsonParserOptimized.py eth LINK 0x514910771af9ca656af840dff83e8264ecf986ca`
- `python3 jsonParserOptimized.py eth SHIB 0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce`
- `python3 jsonParserOptimized.py eth MKR 0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2`
- `python3 jsonParserOptimized.py polygon LINK 0x53e0bca35ec356bd5dddfebbd1fc0fd03fabad39`
- `python3 jsonParserOptimized.py polygon MKR 0x6f7C932e7684666C9fd1d44527765433e01fF61d`
- `python3 jsonParserOptimized.py polygon SHIB 0x6f8a06447ff6fcf75d803135a7de15ce88c1d4ec`

Note: SHIB contract is relatively inactive on Polygon (need to check further if the address  correct), so we may want to remove it from our analysis.