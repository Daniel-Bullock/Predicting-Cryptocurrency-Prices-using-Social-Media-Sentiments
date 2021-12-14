import os.path

from web3 import Web3
import json
import sys
import time
import pickle
from tqdm import tqdm

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: jsonParserOptimized.py blockchain-name(eth or polygon) token-ticker token-address")
        sys.exit(1)

    blockchain = sys.argv[1]
    if blockchain == "eth":
        api_url = 'https://mainnet.infura.io/v3/b40beb8540af492e968e6b67952443cc' #Account 1
        #api_url = 'https://mainnet.infura.io/v3/e2d4c3def23c4f79a7b0b0620b1ed8b7' #Account 2
        #api_url = 'https://mainnet.infura.io/v3/17d53ab55e7047b7b00f03c3aed7ec89' #Account 3
        #api_url = 'https://mainnet.infura.io/v3/e4a15174f6304761a228fdbbef0b7ff2' #Account 4
    elif blockchain == "polygon":
        api_url = 'https://polygon-mainnet.infura.io/v3/74a63497e0374a9abdbb90d60d1fd4e3'
    else:
        print("incorrect blockchain identifier")
        sys.exit(1)
    token_ticker = sys.argv[2]

    w3 = Web3(Web3.HTTPProvider(api_url)) #Conenct to JSON-RPC HTTP service at Infuria

    tokenAddress = Web3.toChecksumAddress(sys.argv[3]) #Contract address
    with open('contracts/LINK/abi.json') as f: #Chainlink ABI (ERC 667) from https://github.com/smartcontractkit/LinkToken/tree/master/contracts/v0.6
        tokenAbi = json.loads(f.read())
    tokenContract = w3.eth.contract(address=tokenAddress, abi=tokenAbi)

    jsonFile = open("data/" + token_ticker + "-" + blockchain + "-transfer-state-final.json",'r') #Source data file with token trasfer data
    records = json.load(jsonFile)

    balanceDict = {}
    transferFromBalance = [] #List that stores the current balance of accounts that sent tokens
    transferToBalance = [] ##List that stores the current balance of accounts that received tokens
    transferValueList = []  #List that stores the time series of transfer values
    timestampList = []
    processedBlocks = []
    lastStoredBlock = 0

    pickle_file = "data/" + token_ticker + "_" + blockchain + "_transfer_list_final.pickle"

    queryCounter=0
    maxQuery=70000

    if os.path.isfile(pickle_file):
        stored_var = pickle.load(open(pickle_file, 'rb'))
        timestampList = stored_var["timeStampList"]
        transferValueList = stored_var["transferValueList"]
        transferFromBalance = stored_var["transferFromBalanceList"]
        transferToBalance = stored_var["transferToBalanceList"]
        processedBlocks = stored_var["processedBlocks"]
        lastStoredBlock = int(processedBlocks[-1])

    stored_vars={}
    stored_vars["timeStampList"] = timestampList
    stored_vars["transferValueList"] = transferValueList
    stored_vars["transferFromBalanceList"] = transferFromBalance
    stored_vars["transferToBalanceList"] = transferToBalance
    stored_vars["processedBlocks"] = processedBlocks

    def saveDict():
        with open(pickle_file,'wb') as handle:
            pickle.dump(stored_vars, handle, protocol = pickle.HIGHEST_PROTOCOL)

    for blockNumber in tqdm(records["blocks"]):
        if int(blockNumber) >= lastStoredBlock:
            processedBlocks.append(int(blockNumber))
            for transactionHash in records["blocks"][blockNumber]:
                for logIndex in records["blocks"][blockNumber][transactionHash]:
                    transferValueList.append(records["blocks"][blockNumber][transactionHash][logIndex]["value"])
                    timestampList.append(records["blocks"][blockNumber][transactionHash][logIndex]["timestamp"])
                    fromAccount = Web3.toChecksumAddress(records["blocks"][blockNumber][transactionHash][logIndex]["from"])
                    toAccount = Web3.toChecksumAddress(records["blocks"][blockNumber][transactionHash][logIndex]["to"])
                    if fromAccount not in balanceDict:
                        balanceDict[fromAccount] = w3.fromWei(tokenContract.functions.balanceOf(fromAccount).call(), 'ether')
                        queryCounter += 1
                    if toAccount not in balanceDict:
                        balanceDict[toAccount] = w3.fromWei(tokenContract.functions.balanceOf(toAccount).call(), 'ether')
                        queryCounter += 1
                    transferFromBalance.append(balanceDict[fromAccount])
                    transferToBalance.append(balanceDict[toAccount])
                    if queryCounter>=maxQuery:
                        saveDict()
                        sys.exit(1)

    saveDict()
